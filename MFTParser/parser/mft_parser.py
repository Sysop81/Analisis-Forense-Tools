import struct
from tqdm import tqdm
from models.parsed_mft_record import ParsedMFTRecord
from helpers.tools import Utils
from display.dhandler import Display

class MFTParser:
    
    _SEQUENCE_NUMBER_OFFSET = 16 # Offset 16-17: Sequence Number (2 bytes, little endian)
    _SEQUENCE_NUMBER_SHIFT = 48  # Bits to shift SequenceNumber into the upper 16 bits of MFT Reference
    _FLAGS_OFFSET = 22           # Offset 22-23: 2 bytes
    _INFORMATION_ATTR_OFFSET = 56 # Offset to start attribute search

    _STANDARD_INFO_CREATION_OFFSET = 0x00       # HEX VALUE (DECIMAL = 0)
    _STANDARD_INFO_MODIFICATION_OFFSET = 0x08   # HEX VALUE (DECIMAL = 8)
    _STANDARD_INFO_MFT_MOD_OFFSET = 0x10        # HEX VALUE (DECIMAL = 16)
    _STANDARD_INFO_ACCESS_OFFSET = 0x18         # HEX VALUE (DECIMAL = 24)

    _FILE_NAME_INFO_CREATION_OFFSET = 0x08       # HEX VALUE (DECIMAL = 8)
    _FILE_NAME_INFO_MODIFICATION_OFFSET = 0x10   # HEX VALUE (DECIMAL = 16)
    _FILE_NAME_INFO_MFT_MOD_OFFSET = 0x18        # HEX VALUE (DECIMAL = 24)
    _FILE_NAME_INFO_ACCESS_OFFSET = 0x20         # HEX VALUE (DECIMAL = 32)

    # FILE_NAME namespaces
    _NAMESPACES = {
        0: "POSIX",
        1: "WIN32",
        2: "DOS",
        3: "WIN32_DOS",
    }
    
    def __init__(self) -> None:
        self._parsed_record_list : list[ParsedMFTRecord] = []

    @property
    def parsed_record_list(self):
        return self._parsed_record_list   

    def append_record(self,record : bytes, entry_number : int):
        try:
            
            # Instatiate data class
            parsed_record = ParsedMFTRecord()

            # Getting the record attributes from binary stream
            parsed_record.entry_number = entry_number
            parsed_record.sequence_number = self.parse_sequence_number(record)
            parsed_record.mft_reference = self.parse_mft_reference(parsed_record.sequence_number,entry_number)
            parsed_record = self.parse_flags(record,parsed_record)
            parsed_record = self.parse_standard_info(record,parsed_record)
            parsed_record = self.parse_file_name_info(record,parsed_record)
            if not parsed_record._file_name_short and not parsed_record._file_name_large:
                raise ValueError(
                    f"MFT entry {parsed_record.entry_number}: "
                    "FILE_NAME missing (short and long empty)"
                )
            parsed_record = self.parse_data_attribute(record,parsed_record)
            
            # Append to parsed record list
            self._parsed_record_list.append(parsed_record)
            
        except Exception :
            raise   

    def parse_sequence_number(self,record : bytes) -> int:
        return struct.unpack_from("<H", record,self._SEQUENCE_NUMBER_OFFSET)[0]    
    
    def parse_mft_reference(self,sequence_number: int, entry_number : int) : 
        return (sequence_number << self._SEQUENCE_NUMBER_SHIFT) | entry_number  

    def parse_flags(self,record : bytes,parsed_record: ParsedMFTRecord) -> ParsedMFTRecord:
        flags = struct.unpack_from("<H", record, self._FLAGS_OFFSET)[0]

        parsed_record.IsDirectory = bool(flags & 0x0002)    # Bit 1 directory
        parsed_record.IsHidden = bool(flags & 0x0004)       # Bit 2 hidden
        parsed_record.IsSystem = bool(flags & 0x0008)       # Bit 3 System file
        parsed_record.IsReadOnly = bool(flags & 0x0001)     # Bit 0 Read only

        return parsed_record
    
    def parse_standard_info(self,record : bytes,parsed_record : ParsedMFTRecord) -> ParsedMFTRecord:
        # Get initial offset for loop    
        offset = self._INFORMATION_ATTR_OFFSET

        # Iterate until the end of the record
        while offset < len(record):
            
            # bynary reading in little endian 4 bytes and extract the value for the tuple
            attr_type = struct.unpack_from("<I", record, offset)[0]
            
            # Check end of attributes in the MFT record
            if attr_type == 0xFFFFFFFF:
                break

            attr_length = struct.unpack_from("<I", record, offset + 4)[0]
            
            if attr_type == ParsedMFTRecord.ATTR_STANDARD_INFORMATION:
                content_offset = struct.unpack_from("<H", record, offset + 20)[0]
                content = record[offset + content_offset: offset + attr_length]
                
                creation = struct.unpack_from("<Q", content, self._STANDARD_INFO_CREATION_OFFSET)[0] # 0
                modification = struct.unpack_from("<Q", content, self._STANDARD_INFO_MODIFICATION_OFFSET)[0] # 8
                mft_mod = struct.unpack_from("<Q", content, self._STANDARD_INFO_MFT_MOD_OFFSET)[0] # 16
                access = struct.unpack_from("<Q", content, self._STANDARD_INFO_ACCESS_OFFSET)[0] # 24
            
                parsed_record._0x10Creation= Utils.filetime_to_dt(creation)
                parsed_record._0x10Modification = Utils.filetime_to_dt(modification)
                parsed_record._0x10MFTModification = Utils.filetime_to_dt(mft_mod)
                parsed_record._0x10Access = Utils.filetime_to_dt(access)

            offset += attr_length
            
            # Check legth to avoid infinite loop
            if(attr_length == 0): break
            
        return parsed_record    
    
    def parse_file_name_info(self,record : bytes,parse_record : ParsedMFTRecord) -> ParsedMFTRecord:
        
        # By default empty file names
        parse_record.file_name_short = ""
        parse_record.file_name_large = ""
        parse_record.name_type = ""
        namespaceslist = []
        offset = self._INFORMATION_ATTR_OFFSET
        
        while offset < len(record):
            attr_type = struct.unpack_from("<I", record, offset)[0]
            if attr_type == 0xFFFFFFFF:
                break
            attr_length = struct.unpack_from("<I", record, offset + 4)[0]
            non_resident_flag = struct.unpack_from("<B", record, offset + 8)[0]

            if attr_type == ParsedMFTRecord.ATTR_FILE_NAME and non_resident_flag == 0:
                content_offset = struct.unpack_from("<H", record, offset + 20)[0]
                content = record[offset + content_offset : offset + attr_length]

                # Getting parent reference
                parse_record.parent_mft_reference = struct.unpack_from("<Q", content, 0)[0]
                
                # Getting File Name & namespace
                name_length = struct.unpack_from("<B", content, 0x40)[0]
                name_namespace = struct.unpack_from("<B", content, 0x41)[0]
                name_bytes = content[0x42 : 0x42 + name_length*2]

                # File Name Timestamps
                creation = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_CREATION_OFFSET)[0] # 8
                modification = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_MODIFICATION_OFFSET)[0] # 16
                mft_mod = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_MFT_MOD_OFFSET)[0] # 24
                access = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_ACCESS_OFFSET)[0] # 32

                # Appedd to record object
                parse_record._0x30Creation = Utils.filetime_to_dt(creation)
                parse_record._0x30Modification = Utils.filetime_to_dt(modification)
                parse_record._0x30MFTModification = Utils.filetime_to_dt(mft_mod)
                parse_record._0x30Access = Utils.filetime_to_dt(access)

                # Getting file names short and long and append all namespaces
                if isinstance(name_bytes, (bytes, bytearray)) and len(name_bytes) % 2 == 0:
                    decoded_file_name = Utils.clean_string(name_bytes.decode("utf-16le", errors="ignore")) 
                    namespaceslist.append(name_namespace)
                    if name_namespace == 0: # POSIX
                        parse_record.file_name_short = decoded_file_name
                        parse_record._file_name_large = decoded_file_name

                    elif name_namespace in (1,3): # Win32 OR Win32 + DOS [Long name]    
                        parse_record._file_name_large = decoded_file_name
                        
                        if not parse_record._file_name_short :
                            parse_record._file_name_short = decoded_file_name

                    elif name_namespace == 2: # Dos [Short name]
                        
                        parse_record._file_name_short = decoded_file_name
                        if not parse_record._file_name_large:
                            parse_record._file_name_large = decoded_file_name

            offset += attr_length
            if(attr_length == 0): break

        # Build object namespaces
        for index,ns in enumerate(namespaceslist):
            parse_record.name_type += self._NAMESPACES[ns]
            if index < len(namespaceslist) - 1:
                parse_record.name_type += " | "
        
        return parse_record 
    
    def parse_data_attribute(self,record : bytes,parse_record : ParsedMFTRecord) -> ParsedMFTRecord:
        
        data = {
            "ads_files" : [],
            "IsADS":False
        }
        
        offset = self._INFORMATION_ATTR_OFFSET
        
        while offset < len(record):
            attr_type = struct.unpack_from("<I", record, offset)[0]
            if attr_type == 0xFFFFFFFF:
                break
            attr_length = struct.unpack_from("<I", record, offset + 4)[0]
            
            if attr_type == ParsedMFTRecord.ATTR_DATA:
                
                # Get stream name
                name_length = struct.unpack_from("<B", record, offset + 9)[0]
                if name_length > 0:
                    name_bytes = record[offset + 0x40 : offset + 0x40 + name_length*2]
                    try:
                        name = name_bytes.decode("utf-16le")
                        if not Utils.has_non_printable_chars(name): 
                            data["ads_files"].append(Utils.clean_string(name))
                    except:
                        name = "<error decoding stream name>"
                # else:
                #     name = "(MAIN STREAM)"
            offset += attr_length

        parse_record.IsADS = len(data["ads_files"]) > 0
        parse_record.ADSFiles = ",".join(data["ads_files"])
        
        return parse_record 
    
    def build_paths(self) -> None:
        ref_map = {r.mft_reference: r for r in self.parsed_record_list}
        progress_bar = tqdm(
            total = len(self.parsed_record_list),
            desc = f"{Display.print_color_text('Processing PATHs',Display.YELLOW)}",
            unit="records",
            dynamic_ncols = True,
            colour = "GREEN"
        )

        for record in self.parsed_record_list:
            current = record.mft_reference
            parent_rf = record.parent_mft_reference
            path_parts = []

            visited = {current}

            # path_parts.append(
            #     record.file_name_large
            #     or record.file_name_short
            #     or f"MFT_{record.mft_reference}"
            # )

            while True:
                if parent_rf == current:
                    break

                if parent_rf not in ref_map:
                    break

                if parent_rf in visited:
                    break

                visited.add(parent_rf)

                current = parent_rf
                new_record = ref_map[current]

                path_parts.append(
                    new_record.file_name_large
                    or new_record.file_name_short
                    or f"MFT_{record.mft_reference}"
                )

                parent_rf = new_record.parent_mft_reference

            # build fianl Parent PATH 
            record.path = "\\".join(reversed(path_parts))
            if not record.path.startswith("."):
                record.path = ".\\" + record.path

            # Update progress bar
            progress_bar.update(1)    
        progress_bar.set_postfix_str(Display.print_color_text("Done",Display.GREEN), refresh=True)
        progress_bar.close()         
            