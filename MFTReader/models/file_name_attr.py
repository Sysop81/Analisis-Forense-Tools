class FileNameInfo:

    # FILE_NAME namespaces
    _NAMESPACES = {
        0: "POSIX",
        1: "WIN32",
        2: "DOS",
        3: "WIN32_DOS",
    }

    def __init__(self):
        self._file_name = None
        self._namespace = None
        self._0x30Creation = None
        self._0x30Modification = None
        self._0x30MFTModification = None
        self._0x30Access = None

    # file_name
    @property
    def file_name(self):
        return self._file_name

    @file_name.setter
    def file_name(self, value):
        self._file_name = value

    # namespace
    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        self._namespace = self._NAMESPACES[value] 

    # 0x30Creation
    @property
    def creation_time(self):
        return self._0x30Creation

    @creation_time.setter
    def creation_time(self, value):
        self._0x30Creation = value

    # 0x30Modification
    @property
    def modification_time(self):
        return self._0x30Modification

    @modification_time.setter
    def modification_time(self, value):
        self._0x30Modification = value

    # 0x30MFTModification
    @property
    def mft_modification_time(self):
        return self._0x30MFTModification

    @mft_modification_time.setter
    def mft_modification_time(self, value):
        self._0x30MFTModification = value

    # 0x30Access
    @property
    def access_time(self):
        return self._0x30Access

    @access_time.setter
    def access_time(self, value):
        self._0x30Access = value

    def to_dict(self)->dict:
        return {
            'FileName' : self._file_name if self._file_name else '',
            'NameType' : self._namespace if self._namespace else '',
            '0x30Creation' : self._0x30Creation.strftime("%Y-%m-%d %H:%M:%S") if self._0x30Creation else '',
            '0x30Modification': self._0x30Modification.strftime("%Y-%m-%d %H:%M:%S") if self._0x30Modification else '',
            '0x30MFTModification' : self._0x30MFTModification.strftime("%Y-%m-%d %H:%M:%S") if self._0x30MFTModification else '',
            '0x30Access' : self._0x30Access.strftime("%Y-%m-%d %H:%M:%S") if self._0x30Access else ''
        }    

    def __str__(self):
        return (
            f"FileNameInfo(\n"
            f"  file_name={self._file_name},\n"
            f"  namespace={self._namespace},\n"
            f"  creation_time={self._0x30Creation},\n"
            f"  modification_time={self._0x30Modification},\n"
            f"  mft_modification_time={self._0x30MFTModification},\n"
            f"  access_time={self._0x30Access}\n"
            f")"
        )