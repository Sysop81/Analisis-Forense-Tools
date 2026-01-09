import struct
from models.parsed_mft_record import ParsedMFTRecord
from helpers.tools import Utils

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
    
    def __init__(self) -> None:
        self._parsed_record_list : list[ParsedMFTRecord] = []
        self._entry_number = 0

    @property
    def parsed_record_list(self):
        return self._parsed_record_list

    @property
    def entry_number(self):
        return self._entry_number    

    def append_record(self,record):
        self.build_record(record)
        self._entry_number += 1    

    def build_record(self,record):
        # Instatiate data class
        parsed_record = ParsedMFTRecord()

        # Getting the record attributes
        parsed_record.entry_number = self.entry_number
        parsed_record.sequence_number = self.parse_sequence_number(record)
        parsed_record.mft_reference = self.parse_mft_reference(parsed_record)
        parsed_record = self.parse_flags(record,parsed_record)
        parsed_record = self.parse_standard_info(record,parsed_record)
        parsed_record = self.parse_file_name_info(record,parsed_record)
        parsed_record = self.parse_data_attribute(record,parsed_record) # PROVISIONAL
        
        # Append to parsed record list
        self._parsed_record_list.append(parsed_record)    

    def parse_sequence_number(self,record : bytearray) -> int:
        return struct.unpack_from("<H", record,self._SEQUENCE_NUMBER_OFFSET)[0]    
    
    def parse_mft_reference(self,_parsed_record: ParsedMFTRecord) -> int:
        return (_parsed_record.sequence_number << self._SEQUENCE_NUMBER_SHIFT) | _parsed_record.entry_number  

    def parse_flags(self,record : bytearray,parsed_record: ParsedMFTRecord) -> ParsedMFTRecord:
        flags = struct.unpack_from("<H", record, self._FLAGS_OFFSET)[0]

        parsed_record.IsDirectory = bool(flags & 0x0002)    # Bit 1 directory
        parsed_record.IsHidden = bool(flags & 0x0004)       # Bit 2 hidden
        parsed_record.IsSystem = bool(flags & 0x0008)       # Bit 3 System file
        parsed_record.IsReadOnly = bool(flags & 0x0001)     # Bit 0 Read only

        return parsed_record
    
    def parse_standard_info(self,record : bytearray,parsed_record : ParsedMFTRecord) -> ParsedMFTRecord:
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
    
    def parse_file_name_info(self,record : bytearray,parse_record : ParsedMFTRecord) -> ParsedMFTRecord:
        
        # By default empty file names
        parse_record._file_name_short = ""
        parse_record._file_name_large = ""
        
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
                
                # Getting File Name
                name_length = struct.unpack_from("<B", content, 0x40)[0]
                name_namespace = struct.unpack_from("<B", content, 0x41)[0]
                name_bytes = content[0x42 : 0x42 + name_length*2]

                # File Name Timestamps
                creation = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_CREATION_OFFSET)[0] # 8
                modification = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_MODIFICATION_OFFSET)[0] # 16
                mft_mod = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_MFT_MOD_OFFSET)[0] # 24
                access = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_ACCESS_OFFSET)[0] # 32

                parse_record._0x30Creation = Utils.filetime_to_dt(creation)
                parse_record._0x30Modification = Utils.filetime_to_dt(modification)
                parse_record._0x30MFTModification = Utils.filetime_to_dt(mft_mod)
                parse_record._0x30Access = Utils.filetime_to_dt(access)


                #testing
                #print(f"{}  FN Parent MFT reference: {parent_ref}")
                # print(f"  FN Creation: {Utils.filetime_to_dt(creation)}")
                # print(f"  FN Modification: {Utils.filetime_to_dt(modification)}")
                # print(f"  FN Modification MFT: {Utils.filetime_to_dt(mft_mod)}")
                # print(f"  FN Access: {Utils.filetime_to_dt(access)}")
                
                # Getting file names short and long
                if isinstance(name_bytes, (bytes, bytearray)) and len(name_bytes) % 2 == 0:
                    decoded_file_name = Utils.clean_string(name_bytes.decode("utf-16le", errors="ignore"))

                    if name_namespace == 2: # Dos [Short name]
                        parse_record._file_name_short = decoded_file_name
                    elif name_namespace in (1,3): # Win32 OR Win32 + DOS [Long name]    
                        parse_record._file_name_large = decoded_file_name
                        if not parse_record._file_name_short :
                            parse_record._file_name_short = parse_record._file_name_large 

            offset += attr_length
            if(attr_length == 0): break

        return parse_record 
    
    def parse_data_attribute(self,record : bytearray,parse_record : ParsedMFTRecord) -> ParsedMFTRecord:
        
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
            non_resident_flag = struct.unpack_from("<B", record, offset + 8)[0]

            if attr_type == ParsedMFTRecord.ATTR_DATA:
                #print(f"ATTR OFFSET -->: {offset}")
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

                # Resident stream
                if non_resident_flag == 0:
                    content_offset = struct.unpack_from("<H", record, offset + 20)[0]  # Resident Value Offset
                    content_length = struct.unpack_from("<I", record, offset + 16)[0]   # Resident Value Length
                    data_bytes = record[offset + content_offset : offset + content_offset + content_length]
                    
                    # print(f"\nATTR $DATA: {name}")
                    # print(f"  SIZE: {content_length} bytes")
                    # print("  CONTENT:")
                    # try:
                    #     print(data_bytes.decode("utf-8", errors='replace'))
                    # except:
                    #     print(data_bytes)

                # Non resident stream
                else:
                    #start_vcn = struct.unpack_from("<Q", record, offset + 16)[0]
                    #end_vcn = struct.unpack_from("<Q", record, offset + 24)[0]
                    # print(f"\nATTR $DATA (NON RESIDENT): {name}")
                    pass
                    

            offset += attr_length

        parse_record.IsADS = len(data["ads_files"]) > 0
        parse_record.ADSFiles = ",".join(data["ads_files"])
        
        return parse_record 
