class ParsedMFTRecord:
    
    ATTR_STANDARD_INFORMATION = 0x10
    ATTR_FILE_NAME = 0x30
    ATTR_DATA = 0x80

    def __init__(self):
        self._entry_number = None
        self._sequence_number = None
        self._mft_reference = None
        self._parent_mft_reference = None
        self._name_type = None
        self._file_name_short = None
        self._file_name_large = None
        self._path = None
        self._IsDirectory = None
        self._IsHidden = None
        self._IsSystem = None
        self._IsReadOnly = None
        self._IsADS = None
        self._ADSFiles = None
        self._0x10Creation = None
        self._0x10Modification = None
        self._0x10MFTModification = None
        self._0x10Access = None
        self._0x30Creation = None
        self._0x30Modification = None
        self._0x30MFTModification = None
        self._0x30Access = None

    # --- Identifiers ---
    @property
    def entry_number(self):
        return self._entry_number

    @entry_number.setter
    def entry_number(self, value):
        self._entry_number = value

    @property
    def sequence_number(self):
        return self._sequence_number

    @sequence_number.setter
    def sequence_number(self, value):
        self._sequence_number = value

    @property
    def mft_reference(self):
        return self._mft_reference

    @mft_reference.setter
    def mft_reference(self, value):
        self._mft_reference = value

    @property
    def parent_mft_reference(self):
        return self._parent_mft_reference

    @parent_mft_reference.setter
    def parent_mft_reference(self, value):
        self._parent_mft_reference = value    

    # --- Path && file names ---
    
    @property
    def name_type(self):
        return self._name_type

    @name_type.setter
    def name_type(self, value):
        self._name_type = value

    @property
    def file_name_short(self):
        return self._file_name_short

    @file_name_short.setter
    def file_name_short(self, value):
        self._file_name_short = value

    @property
    def file_name_large(self):
        return self._file_name_large

    @file_name_large.setter
    def file_name_large(self, value):
        self._file_name_large = value

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value

    # --- Flags ---
    @property
    def IsDirectory(self):
        return self._IsDirectory

    @IsDirectory.setter
    def IsDirectory(self, value):
        self._IsDirectory = value

    @property
    def IsHidden(self):
        return self._IsHidden

    @IsHidden.setter
    def IsHidden(self, value):
        self._IsHidden = value

    @property
    def IsSystem(self):
        return self._IsSystem

    @IsSystem.setter
    def IsSystem(self, value):
        self._IsSystem = value

    @property
    def IsReadOnly(self):
        return self._IsReadOnly

    @IsReadOnly.setter
    def IsReadOnly(self, value):
        self._IsReadOnly = value

    @property
    def IsADS(self):
        return self._IsADS

    @IsADS.setter
    def IsADS(self, value):
        self._IsADS = value

    @property
    def ADSFiles(self):
        return self._ADSFiles

    @ADSFiles.setter
    def ADSFiles(self, value):
        self._ADSFiles = value

    # --- $STANDARD_INFORMATION (0x10) ---
    @property
    def standard_info_creation(self):
        return self._0x10Creation

    @standard_info_creation.setter
    def standard_info_creation(self, value):
        self._0x10Creation = value

    @property
    def standard_info_modification(self):
        return self._0x10Modification

    @standard_info_modification.setter
    def standard_info_modification(self, value):
        self._0x10Modification = value

    @property
    def standard_info_mft_modification(self):
        return self._0x10MFTModification

    @standard_info_mft_modification.setter
    def standard_info_mft_modification(self, value):
        self._0x10MFTModification = value

    @property
    def standard_info_access(self):
        return self._0x10Access

    @standard_info_access.setter
    def standard_info_access(self, value):
        self._0x10Access = value

    # --- $FILE_NAME (0x30) ---
    @property
    def file_name_creation(self):
        return self._0x30Creation

    @file_name_creation.setter
    def file_name_creation(self, value):
        self._0x30Creation = value

    @property
    def file_name_modification(self):
        return self._0x30Modification

    @file_name_modification.setter
    def file_name_modification(self, value):
        self._0x30Modification = value

    @property
    def file_name_mft_modification(self):
        return self._0x30MFTModification

    @file_name_mft_modification.setter
    def file_name_mft_modification(self, value):
        self._0x30MFTModification = value

    @property
    def file_name_access(self):
        return self._0x30Access

    @file_name_access.setter
    def file_name_access(self, value):
        self._0x30Access = value

    def to_dict(self):
        return {
            "entry_number": self._entry_number,
            "sequence_number": self._sequence_number,
            "mft_reference": self._mft_reference,
            "parent_mft_reference": self._parent_mft_reference,
            "name_type": self._name_type,
            "file_name_short": self._file_name_short,
            "file_name_large": self._file_name_large,
            "path": self._path,
            "IsDirectory": self._IsDirectory,
            "IsHidden": self._IsHidden,
            "IsSystem": self._IsSystem,
            "IsReadOnly": self._IsReadOnly,
            "ContainsADS": self._IsADS,
            "ADSFiles": self._ADSFiles,
            "0x10Creation": self._0x10Creation,
            "0x10Modification": self._0x10Modification,
            "0x10MFTModification": self._0x10MFTModification,
            "0x10Access": self._0x10Access,
            "0x30Creation": self._0x30Creation,
            "0x30Modification": self._0x30Modification,
            "0x30MFTModification": self._0x30MFTModification,
            "0x30Access": self._0x30Access,
        }    

    def __str__(self):
        return (
            f"ParsedMFTRecord(entry_number={self.entry_number}, "
            f"sequence_number={self.sequence_number}, "
            f"mft_reference={self.mft_reference}, "
            f"parent_mft_reference={self.parent_mft_reference}, "
            f"name_type={self.name_type}, "
            f"file_name_short='{self.file_name_short}', "
            f"file_name_large='{self.file_name_large}', "
            f"path='{self.path}', "
            f"IsDirectory={self.IsDirectory}, "
            f"IsHidden={self.IsHidden}, "
            f"IsSystem={self.IsSystem}, "
            f"IsReadOnly={self.IsReadOnly}, "
            f"IsADS={self.IsADS}, "
            f"ADSFiles={self.ADSFiles}, "
            f"_0x10Creation={self._0x10Creation}, "
            f"_0x10Modification={self._0x10Modification}, "
            f"_0x10MFTModification={self._0x10MFTModification}, "
            f"_0x10Access={self._0x10Access}, "
            f"_0x30Creation={self._0x30Creation}, "
            f"_0x30Modification={self._0x30Modification}, "
            f"_0x30MFTModification={self._0x30MFTModification}, "
            f"_0x30Access={self._0x30Access})"
        )    