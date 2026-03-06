import struct
#from tqdm import tqdm
from datetime import datetime
from models.parsed_mft_record import ParsedMFTRecord
from models.file_name_attr import FileNameInfo
from models.data_attr import DataInfo
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

    def __init__(self,entry_number : int,_record : bytearray) -> None:
        self._entry_number = entry_number
        self._record = _record
        self._record_structure_list : list[MFTRecordStruct] = []
        self._parsed_record : ParsedMFTRecord = ParsedMFTRecord()
        self._file_name_attr_list : list[FileNameInfo] = []
        self._data_attr_list : list[DataInfo] = []

    @property
    def entry_number(self):
        return self._entry_number    
    
    @property
    def record_structure_list(self):
        return self._record_structure_list
    
    @property
    def parsed_record(self):
        return self._parsed_record
    
    @property
    def file_name_attr_list(self):
        return self._file_name_attr_list
    
    @property
    def data_attr_list(self):
        return self._data_attr_list
    
    def get_standard_info(self) -> dict:
        return {
            '0x10Creation' : self.parsed_record.standard_info_creation.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.standard_info_creation else '',
            '0x10Modification': self.parsed_record.standard_info_modification.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.standard_info_modification else '',
            '0x10MFTModification' : self.parsed_record.standard_info_mft_modification.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.standard_info_mft_modification else '',
            '0x10Access' : self.parsed_record.standard_info_access.strftime("%Y-%m-%d %H:%M:%S") if self.parsed_record.standard_info_access else ''
        }
    
    def get_general_info(self)->dict:
        return {
            'EntryNumber' : self._entry_number,
            'MFTReference': self._parsed_record.mft_reference,
            'ParentMFTRef': self._parsed_record._parent_mft_reference,
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
            i += attr_len  

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

                # Instantiate FileNameInfo class
                file_name_info : FileNameInfo = FileNameInfo()

                # Getting parent reference
                self._parsed_record.parent_mft_reference = struct.unpack_from("<Q", content, 0)[0]
                
                # Getting File Name & namespace
                name_length = struct.unpack_from("<B", content, 0x40)[0]
                name_namespace = struct.unpack_from("<B", content, 0x41)[0]
                file_name_info.namespace = name_namespace
                name_bytes = content[0x42 : 0x42 + name_length*2]

                # File Name Timestamps
                creation = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_CREATION_OFFSET)[0] # 8
                modification = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_MODIFICATION_OFFSET)[0] # 16
                mft_mod = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_MFT_MOD_OFFSET)[0] # 24
                access = struct.unpack_from("<Q", content, self._FILE_NAME_INFO_ACCESS_OFFSET)[0] # 32

                # Appedd to record object
                
                file_name_info.creation_time = Utils.filetime_to_dt(creation)
                file_name_info.modification_time = Utils.filetime_to_dt(modification)
                file_name_info.mft_modification_time = Utils.filetime_to_dt(mft_mod)
                file_name_info.access_time = Utils.filetime_to_dt(access)

                # Getting file names short and long and append all namespaces
                if isinstance(name_bytes, (bytes, bytearray)) and len(name_bytes) % 2 == 0:
                    decoded_file_name = Utils.clean_string(name_bytes.decode("utf-16le", errors="ignore"))
                    file_name_info.file_name = decoded_file_name 
                    
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

                # Append to list
                self._file_name_attr_list.append(file_name_info)

            offset += attr_length
            if(attr_length == 0): break

    # def build_ads_files(self):
    #     # TODO COMPLETE THIS
    #     pass

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
            non_resident_flag = struct.unpack_from("<B", self._record, offset + 8)[0]
            
            if attr_type == ParsedMFTRecord.ATTR_DATA:
                
                # Get stream name
                name_length = struct.unpack_from("<B", self._record, offset + 9)[0]
                attr_name_offset = struct.unpack_from("<H", self._record, offset + 10)[0]
                name : str = ''
                if name_length > 0:
                    name_start = offset + attr_name_offset
                    name_end = name_start + name_length * 2
                    name_bytes = self._record[name_start:name_end]
                    
                    try:
                        name = name_bytes.decode("utf-16le") # utf-16le utf-8
                        data["ads_files"].append(Utils.clean_string(name))
                    except:
                        name = 'UNKNOWN'
                        pass

                    # Build DATA Info object    
                    data_info_attr = DataInfo()
                    
                    # Resident data (ADS)
                    if non_resident_flag == 0:
                        content_offset = struct.unpack_from("<H", self._record, offset + 20)[0]  # Resident Value Offset
                        content_length = struct.unpack_from("<I", self._record, offset + 16)[0]   # Resident Value Length
                        data_bytes = self._record[offset + content_offset : offset + content_offset + content_length]
                        
                        data_info_attr.name = f"{name} (RESIDENT)"
                        data_info_attr.size = f"{content_length} bytes"
                        content : str = ''
                        try:
                            content = data_bytes.decode("utf-8", errors='replace') #
                        except:
                            pass

                        data_info_attr.content = content    
                        
                    # NON Resident stream
                    else:
                        start_vcn = struct.unpack_from("<Q", self._record, offset + 16)[0]
                        end_vcn = struct.unpack_from("<Q", self._record, offset + 24)[0]
                        size = struct.unpack_from("<Q", self._record, offset + 0x30)[0]
                        
                        data_info_attr.name = f"{name} (NON RESIDENT)"
                        data_info_attr.size = f"{size} bytes"
                        data_info_attr.content = f"VCN {start_vcn}-{end_vcn}"

                    self._data_attr_list.append(data_info_attr)    

            offset += attr_length

        self._parsed_record.IsADS = len(data["ads_files"]) > 0
        self.parsed_record.ADSFiles = ",".join(data["ads_files"])       
            