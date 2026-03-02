import struct
#from tqdm import tqdm
from datetime import datetime
from models.parsed_mft_record import ParsedMFTRecord
from models.mft_record_struct import MFTRecordStruct
from helpers.tools import Utils
from display.dhandler import Display

class MFTReader:
    
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
    
    def __init__(self,entry_number : int,_record : bytearray) -> None:
        self._entry_number = entry_number
        self._record = _record
        self._record_structure_list : list[MFTRecordStruct] = []
        self._parsed_record : ParsedMFTRecord = ParsedMFTRecord()

    @property
    def entry_number(self):
        return self._entry_number    
    
    @property
    def record_structure_list(self):
        return self._record_structure_list
    
    @property
    def parsed_record(self):
        return self._parsed_record
    
    def get_standard_info(self) -> dict:
        return {
            '0x10Creation' : self.parsed_record.standard_info_creation.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.standard_info_creation else None,
            '0x10Modification': self.parsed_record.standard_info_modification.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.standard_info_modification else None,
            '0x10MFTModification' : self.parsed_record.standard_info_mft_modification.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.standard_info_mft_modification else None,
            '0x10Access' : self.parsed_record.standard_info_access.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.standard_info_access else None
        }
    
    def get_filename_info(self) ->dict:
        return {
            '0x30Creation' : self.parsed_record.file_name_creation.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.file_name_creation else None,
            '0x30Modification': self.parsed_record.file_name_modification.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.file_name_modification else None,
            '0x30MFTModification' : self.parsed_record.file_name_mft_modification.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.file_name_mft_modification else None,
            '0x30Access' : self.parsed_record.file_name_access.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.file_name_access else None
        }
    
    def get_general_info(self)->dict:
        return {
            'EntryNumber' : self._entry_number,
            'MFTReference': self._parsed_record.mft_reference,
            'FilenNameShort' : self.parsed_record.file_name_short,
            'FileNameLarge': self.parsed_record.file_name_large
        }    
    
    def get_file_flags(self)->dict:
        return {
            'IsDirectory' : str(bool(self._parsed_record.IsDirectory)),
            'IsHidden'    : str(bool(self._parsed_record.IsHidden)),
            'IsSystem'    : str(bool(self._parsed_record.IsSystem)),
            'IsReadOnly'  : str(bool(self._parsed_record.IsReadOnly))  
        }

        
    # def build_attributes(self) -> None:
    #     pass

    def parse_sequence_number(self) -> None:
        self._parsed_record.sequence_number = struct.unpack_from("<H", self._record, self._SEQUENCE_NUMBER_OFFSET)[0]    
    
    def parse_mft_reference(self,sequence_number: int, entry_number : int) : 
        self._parsed_record.mft_reference = (sequence_number << self._SEQUENCE_NUMBER_SHIFT) | self._entry_number  

    def build_general_info(self):
        # Sequence Number
        self._parsed_record.sequence_number = struct.unpack_from("<H", self._record, self._SEQUENCE_NUMBER_OFFSET)[0]
        
        # MFT Reference
        self._parsed_record.mft_reference = (self._parsed_record.sequence_number << self._SEQUENCE_NUMBER_SHIFT) | int(self._entry_number)
        
        # Flags

    def build_file_flags(self):
        flags = struct.unpack_from("<H", self._record, self._FLAGS_OFFSET)[0]

        self._parsed_record.IsDirectory = bool(flags & 0x0002)    # Bit 1 directory
        self._parsed_record.IsHidden = bool(flags & 0x0004)       # Bit 2 hidden
        self._parsed_record.IsSystem = bool(flags & 0x0008)       # Bit 3 System file
        self._parsed_record.IsReadOnly = bool(flags & 0x0001)     # Bit 0 Read only

    def build_record_struct(self):
        
        #print(f"{'Start':>5} {'End':>5} {'Length':>10} {'Type':<10} {'ATTR':<25}")

        types = {
            0x10: "$STANDARD_INFORMATION",
            0x20: "$ATTRIBUTE_LIST",
            0x30: "$FILE_NAME",
            0x40: "$OBJECT_ID",
            0x80: "$DATA",
        }

        # Offset to first attribute (2 bytes at 0x14)
        first_attr = int.from_bytes(self._record[0x14:0x16], "little")

        i = first_attr

        while i + 8 <= 1024: # TODO MOVE LITERAL TO SINGLETONE  
            attr_type = int.from_bytes(self._record[i:i+4], "little")

            # END marker
            if attr_type == 0xFFFFFFFF:
                break

            attr_len = int.from_bytes(self._record[i+4:i+8], "little")

            # Sanity checks. TODO CHECK THIS AND BUILD EMPTHY LIST
            if attr_len < 24 or i + attr_len > 1024:
                print(f"[!] Invalid attribute in offset {i}, size={attr_len}")
                break

            name = types.get(attr_type, "UNKNOWN")
            if name in types.values():
                self._record_structure_list.append(
                    MFTRecordStruct(
                        start_offset = i,
                        end_offset = (i + attr_len - 1),
                        length = attr_len,
                        type= f"0x{attr_type:08X}",
                        attr= name
                    )
                )
                # print(f"{i:5} {(i + attr_len - 1):5} "
                #      f"{attr_len:10} 0x{attr_type:08X} {name:<25}")

            i += attr_len
        # for r in self._record_structure_list:
        #     print(r)    

    def build_standard_info(self):
        # Get initial offset for loop    
        offset = self._INFORMATION_ATTR_OFFSET

        # Iterate until the end of the record
        while offset < len(self._record):
            
            # bynary reading in little endian 4 bytes and extract the value for the tuple
            attr_type = struct.unpack_from("<I", self._record, offset)[0]
            
            # Check end of attributes in the MFT record
            if attr_type == 0xFFFFFFFF:
                break

            attr_length = struct.unpack_from("<I", self._record, offset + 4)[0]
            
            if attr_type == ParsedMFTRecord.ATTR_STANDARD_INFORMATION:
                content_offset = struct.unpack_from("<H", self._record, offset + 20)[0]
                content = self._record[offset + content_offset: offset + attr_length]
                
                creation = struct.unpack_from("<Q", content, self._STANDARD_INFO_CREATION_OFFSET)[0] # 0
                modification = struct.unpack_from("<Q", content, self._STANDARD_INFO_MODIFICATION_OFFSET)[0] # 8
                mft_mod = struct.unpack_from("<Q", content, self._STANDARD_INFO_MFT_MOD_OFFSET)[0] # 16
                access = struct.unpack_from("<Q", content, self._STANDARD_INFO_ACCESS_OFFSET)[0] # 24
            
                self._parsed_record._0x10Creation= Utils.filetime_to_dt(creation)
                self._parsed_record._0x10Modification = Utils.filetime_to_dt(modification)
                self._parsed_record._0x10MFTModification = Utils.filetime_to_dt(mft_mod)
                self._parsed_record._0x10Access = Utils.filetime_to_dt(access)

            offset += attr_length
            
            # Check legth to avoid infinite loop
            if(attr_length == 0): break

    def build_file_name_info(self):
        # By default empty file names
        self._parsed_record.file_name_short = ""
        self._parsed_record.file_name_large = ""
        self._parsed_record.name_type = ""
        namespaceslist = []
        offset = self._INFORMATION_ATTR_OFFSET
        
        while offset < len(self._record):
            attr_type = struct.unpack_from("<I", self._record, offset)[0]
            if attr_type == 0xFFFFFFFF:
                break
            attr_length = struct.unpack_from("<I", self._record, offset + 4)[0]
            non_resident_flag = struct.unpack_from("<B", self._record, offset + 8)[0]

            if attr_type == ParsedMFTRecord.ATTR_FILE_NAME and non_resident_flag == 0:
                content_offset = struct.unpack_from("<H", self._record, offset + 20)[0]
                content = self._record[offset + content_offset : offset + attr_length]

                # Getting parent reference
                self._parsed_record.parent_mft_reference = struct.unpack_from("<Q", content, 0)[0]
                
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
                self._parsed_record._0x30Creation = Utils.filetime_to_dt(creation)
                self._parsed_record._0x30Modification = Utils.filetime_to_dt(modification)
                self._parsed_record._0x30MFTModification = Utils.filetime_to_dt(mft_mod)
                self._parsed_record._0x30Access = Utils.filetime_to_dt(access)

                # Getting file names short and long and append all namespaces
                if isinstance(name_bytes, (bytes, bytearray)) and len(name_bytes) % 2 == 0:
                    decoded_file_name = Utils.clean_string(name_bytes.decode("utf-16le", errors="ignore")) 
                    namespaceslist.append(name_namespace)
                    if name_namespace == 0: # POSIX
                        self._parsed_record.file_name_short = decoded_file_name
                        self._parsed_record._file_name_large = decoded_file_name

                    elif name_namespace in (1,3): # Win32 OR Win32 + DOS [Long name]    
                        self._parsed_record._file_name_large = decoded_file_name
                        
                        if not self._parsed_record._file_name_short :
                            self._parsed_record._file_name_short = decoded_file_name

                    elif name_namespace == 2: # Dos [Short name]
                        
                        self._parsed_record._file_name_short = decoded_file_name
                        if not self._parsed_record._file_name_large:
                            self._parsed_record._file_name_large = decoded_file_name

            offset += attr_length
            if(attr_length == 0): break

        # Build object namespaces
        for index,ns in enumerate(namespaceslist):
            self._parsed_record.name_type += self._NAMESPACES[ns]
            if index < len(namespaceslist) - 1:
                self._parsed_record.name_type += " | "

    def build_ads_files(self):
        # TODO COMPLETE THIS
        pass

    def build_data_info(self):
        data = {
            "ads_files" : [],
            "IsADS":False
        }
        
        offset = self._INFORMATION_ATTR_OFFSET
        
        while offset < len(self._record):
            attr_type = struct.unpack_from("<I", self._record, offset)[0]
            if attr_type == 0xFFFFFFFF:
                break
            attr_length = struct.unpack_from("<I", self._record, offset + 4)[0]
            
            if attr_type == ParsedMFTRecord.ATTR_DATA:
                
                # Get stream name
                name_length = struct.unpack_from("<B", self._record, offset + 9)[0]
                if name_length > 0:
                    name_bytes = self._record[offset + 0x40 : offset + 0x40 + name_length*2]
                    try:
                        name = name_bytes.decode("utf-16le")
                        data["ads_files"].append(Utils.clean_string(name))
                        # This code is for MFTPrse app. now is checking without clean characteres
                        # if not Utils.has_non_printable_chars(name): 
                        #     data["ads_files"].append(Utils.clean_string(name))
                    except:
                        name = "<error decoding stream name>"
                # else:
                #     name = "(MAIN STREAM)"
            offset += attr_length

        self._parsed_record.IsADS = len(data["ads_files"]) > 0
        self.parsed_record.ADSFiles = ",".join(data["ads_files"])    


    # @property
    # def parsed_record_list(self):
    #     return self._parsed_record_list   

    # def append_record(self,record : bytes, entry_number : int):
    #     try:
            
    #         # Instatiate data class
    #         parsed_record = ParsedMFTRecord()

    #         # Getting the record attributes from binary stream
    #         parsed_record.entry_number = entry_number
    #         parsed_record.sequence_number = self.parse_sequence_number(record)
    #         parsed_record.mft_reference = self.parse_mft_reference(parsed_record.sequence_number,entry_number)
    #         parsed_record = self.parse_flags(record,parsed_record)
    #         parsed_record = self.parse_standard_info(record,parsed_record)
    #         parsed_record = self.parse_file_name_info(record,parsed_record)
    #         if not parsed_record._file_name_short and not parsed_record._file_name_large:
    #             raise ValueError(
    #                 f"MFT entry {parsed_record.entry_number}: "
    #                 "FILE_NAME missing (short and long empty)"
    #             )
    #         parsed_record = self.parse_data_attribute(record,parsed_record)
            
    #         # Append to parsed record list
    #         self._parsed_record_list.append(parsed_record)
            
    #     except Exception :
    #         raise   

    # def parse_sequence_number(self,record : bytes) -> int:
    #     return struct.unpack_from("<H", record,self._SEQUENCE_NUMBER_OFFSET)[0]    
    
    # def parse_mft_reference(self,sequence_number: int, entry_number : int) : 
    #     return (sequence_number << self._SEQUENCE_NUMBER_SHIFT) | entry_number  

    # def parse_flags(self,record : bytes,parsed_record: ParsedMFTRecord) -> ParsedMFTRecord:
    #     flags = struct.unpack_from("<H", record, self._FLAGS_OFFSET)[0]

    #     parsed_record.IsDirectory = bool(flags & 0x0002)    # Bit 1 directory
    #     parsed_record.IsHidden = bool(flags & 0x0004)       # Bit 2 hidden
    #     parsed_record.IsSystem = bool(flags & 0x0008)       # Bit 3 System file
    #     parsed_record.IsReadOnly = bool(flags & 0x0001)     # Bit 0 Read only

    #     return parsed_record
    
    # def parse_standard_info(self,record : bytes,parsed_record : ParsedMFTRecord) -> ParsedMFTRecord:
    #     # Get initial offset for loop    
    #     offset = self._INFORMATION_ATTR_OFFSET

    #     # Iterate until the end of the record
    #     while offset < len(record):
            
    #         # bynary reading in little endian 4 bytes and extract the value for the tuple
    #         attr_type = struct.unpack_from("<I", record, offset)[0]
            
    #         # Check end of attributes in the MFT record
    #         if attr_type == 0xFFFFFFFF:
    #             break

    #         attr_length = struct.unpack_from("<I", record, offset + 4)[0]
            
    #         if attr_type == ParsedMFTRecord.ATTR_STANDARD_INFORMATION:
    #             content_offset = struct.unpack_from("<H", record, offset + 20)[0]
    #             content = record[offset + content_offset: offset + attr_length]
                
    #             creation = struct.unpack_from("<Q", content, self._STANDARD_INFO_CREATION_OFFSET)[0] # 0
    #             modification = struct.unpack_from("<Q", content, self._STANDARD_INFO_MODIFICATION_OFFSET)[0] # 8
    #             mft_mod = struct.unpack_from("<Q", content, self._STANDARD_INFO_MFT_MOD_OFFSET)[0] # 16
    #             access = struct.unpack_from("<Q", content, self._STANDARD_INFO_ACCESS_OFFSET)[0] # 24
            
    #             parsed_record._0x10Creation= Utils.filetime_to_dt(creation)
    #             parsed_record._0x10Modification = Utils.filetime_to_dt(modification)
    #             parsed_record._0x10MFTModification = Utils.filetime_to_dt(mft_mod)
    #             parsed_record._0x10Access = Utils.filetime_to_dt(access)

    #         offset += attr_length
            
    #         # Check legth to avoid infinite loop
    #         if(attr_length == 0): break
            
    #     return parsed_record    
    
    # def parse_file_name_info(self,record : bytes,parse_record : ParsedMFTRecord) -> ParsedMFTRecord:
        
    #     # By default empty file names
    #     parse_record.file_name_short = ""
    #     parse_record.file_name_large = ""
    #     parse_record.name_type = ""
    #     namespaceslist = []
    #     offset = self._INFORMATION_ATTR_OFFSET
        
    #     while offset < len(record):
    #         attr_type = struct.unpack_from("<I", record, offset)[0]
    #         if attr_type == 0xFFFFFFFF:
    #             break
    #         attr_length = struct.unpack_from("<I", record, offset + 4)[0]
    #         non_resident_flag = struct.unpack_from("<B", record, offset + 8)[0]

    #         if attr_type == ParsedMFTRecord.ATTR_FILE_NAME and non_resident_flag == 0:
    #             content_offset = struct.unpack_from("<H", record, offset + 20)[0]
    #             content = record[offset + content_offset : offset + attr_length]

    #             # Getting parent reference
    #             parse_record.parent_mft_reference = struct.unpack_from("<Q", content, 0)[0]
                
    #             # Getting File Name & namespace
    #             name_length = struct.unpack_from("<B", content, 0x40)[0]
    #             name_namespace = struct.unpack_from("<B", content, 0x41)[0]
    #             name_bytes = content[0x42 : 0x42 + name_length*2]

    #             # File Name Timestamps
    #             creation = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_CREATION_OFFSET)[0] # 8
    #             modification = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_MODIFICATION_OFFSET)[0] # 16
    #             mft_mod = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_MFT_MOD_OFFSET)[0] # 24
    #             access = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_ACCESS_OFFSET)[0] # 32

    #             # Appedd to record object
    #             parse_record._0x30Creation = Utils.filetime_to_dt(creation)
    #             parse_record._0x30Modification = Utils.filetime_to_dt(modification)
    #             parse_record._0x30MFTModification = Utils.filetime_to_dt(mft_mod)
    #             parse_record._0x30Access = Utils.filetime_to_dt(access)

    #             # Getting file names short and long and append all namespaces
    #             if isinstance(name_bytes, (bytes, bytearray)) and len(name_bytes) % 2 == 0:
    #                 decoded_file_name = Utils.clean_string(name_bytes.decode("utf-16le", errors="ignore")) 
    #                 namespaceslist.append(name_namespace)
    #                 if name_namespace == 0: # POSIX
    #                     parse_record.file_name_short = decoded_file_name
    #                     parse_record._file_name_large = decoded_file_name

    #                 elif name_namespace in (1,3): # Win32 OR Win32 + DOS [Long name]    
    #                     parse_record._file_name_large = decoded_file_name
                        
    #                     if not parse_record._file_name_short :
    #                         parse_record._file_name_short = decoded_file_name

    #                 elif name_namespace == 2: # Dos [Short name]
                        
    #                     parse_record._file_name_short = decoded_file_name
    #                     if not parse_record._file_name_large:
    #                         parse_record._file_name_large = decoded_file_name

    #         offset += attr_length
    #         if(attr_length == 0): break

    #     # Build object namespaces
    #     for index,ns in enumerate(namespaceslist):
    #         parse_record.name_type += self._NAMESPACES[ns]
    #         if index < len(namespaceslist) - 1:
    #             parse_record.name_type += " | "
        
    #     return parse_record 
    
    # def parse_data_attribute(self,record : bytes,parse_record : ParsedMFTRecord) -> ParsedMFTRecord:
        
    #     data = {
    #         "ads_files" : [],
    #         "IsADS":False
    #     }
        
    #     offset = self._INFORMATION_ATTR_OFFSET
        
    #     while offset < len(record):
    #         attr_type = struct.unpack_from("<I", record, offset)[0]
    #         if attr_type == 0xFFFFFFFF:
    #             break
    #         attr_length = struct.unpack_from("<I", record, offset + 4)[0]
            
    #         if attr_type == ParsedMFTRecord.ATTR_DATA:
                
    #             # Get stream name
    #             name_length = struct.unpack_from("<B", record, offset + 9)[0]
    #             if name_length > 0:
    #                 name_bytes = record[offset + 0x40 : offset + 0x40 + name_length*2]
    #                 try:
    #                     name = name_bytes.decode("utf-16le")
    #                     if not Utils.has_non_printable_chars(name): 
    #                         data["ads_files"].append(Utils.clean_string(name))
    #                 except:
    #                     name = "<error decoding stream name>"
    #             # else:
    #             #     name = "(MAIN STREAM)"
    #         offset += attr_length

    #     parse_record.IsADS = len(data["ads_files"]) > 0
    #     parse_record.ADSFiles = ",".join(data["ads_files"])
        
    #     return parse_record 
    
    # def build_paths(self) -> None:
    #     ref_map = {r.mft_reference: r for r in self.parsed_record_list}
    #     progress_bar = tqdm(
    #         total = len(self.parsed_record_list),
    #         desc = f"{Display.print_color_text('Processing PATHs',Display.YELLOW)}",
    #         unit="records",
    #         dynamic_ncols = True,
    #         colour = "GREEN"
    #     )

    #     for record in self.parsed_record_list:
    #         current = record.mft_reference
    #         parent_rf = record.parent_mft_reference
    #         path_parts = []

    #         visited = {current}

    #         # path_parts.append(
    #         #     record.file_name_large
    #         #     or record.file_name_short
    #         #     or f"MFT_{record.mft_reference}"
    #         # )

    #         while True:
    #             if parent_rf == current:
    #                 break

    #             if parent_rf not in ref_map:
    #                 break

    #             if parent_rf in visited:
    #                 break

    #             visited.add(parent_rf)

    #             current = parent_rf
    #             new_record = ref_map[current]

    #             path_parts.append(
    #                 new_record.file_name_large
    #                 or new_record.file_name_short
    #                 or f"MFT_{record.mft_reference}"
    #             )

    #             parent_rf = new_record.parent_mft_reference

    #         # build fianl Parent PATH 
    #         record.path = "\\".join(reversed(path_parts))
    #         if not record.path.startswith("."):
    #             record.path = ".\\" + record.path

    #         # Update progress bar
    #         progress_bar.update(1)    
    #     progress_bar.set_postfix_str(Display.print_color_text("Done",Display.GREEN), refresh=True)
    #     progress_bar.close()         
            