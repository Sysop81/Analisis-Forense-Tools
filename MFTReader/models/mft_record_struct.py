class MFTRecordStruct:

    _TYPES = {
        0x10: "$STANDARD_INFORMATION",
        0x20: "$ATTRIBUTE_LIST",
        0x30: "$FILE_NAME",
        0x40: "$OBJECT_ID",
        0x80: "$DATA",
    }



    def __init__(self, start_offset : int, end_offset: int, length : int, type : str, attr : str) -> None:
        self._start_offset : int = start_offset
        self._end_offset : int = end_offset
        self._length : int = length
        self._type : str = type
        self._attr : str = attr

    def __str__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"start_offset={self._start_offset}, "
            f"end_offset={self._end_offset}, "
            f"length={self._length}, "
            f"type='{self._type}', "
            f"attr='{self._attr}'"
            f")"
        )    