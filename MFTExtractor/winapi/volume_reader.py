import ctypes
from display.dhandler import Display
from winapi.ntfs import (kernel32,get_ntfs_info,GENERIC_READ,FILE_SHARE_READ,FILE_SHARE_WRITE,
    OPEN_EXISTING,INVALID_HANDLE_VALUE,RECORD_SIZE)

class VolumeReader:

    def __init__(self,_letter : str):
        self.letter = _letter
        self.path = f"\\\\.\\{self.letter}:"
        self.handle = None
        self.ntfs_info = None
        self.open_volume()
        pass

    """
        Method open_volume
        This method opens an NTFS volume for reading and saves a handle (pointer to vol resource).
        If it cannot open it, it displays an error and terminates the program.
        Resource. https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-createfilew
    """
    def open_volume(self):
        Display.show_info(f" Opening NTFS volume {self.letter}")
        self.handle = kernel32.CreateFileW(
            self.path,
            GENERIC_READ,
            FILE_SHARE_READ | FILE_SHARE_WRITE,
            None,
            OPEN_EXISTING,
            0,
            None
        )
        
        if self.handle == INVALID_HANDLE_VALUE:
            Display.show_error("The volume could not be opened")
            Display.show_end_program(1)

    def close_handle(self):
        kernel32.CloseHandle(self.handle)

    def get_ntfs_info(self):
        Display.show_info(" Getting NTFS information...")
        try:
            self.ntfs_info = get_ntfs_info(self.handle)
            Display.show_ntfs_info(self.ntfs_info)
        except OSError as e:
            Display.show_error(e)
            Display.show_end_program(1)                

    def set_file_pointer(self):
        Display.show_info("Moving the pointer to the start of the MFT")
        offset = self.ntfs_info.MftStartLcn * self.ntfs_info.BytesPerCluster
        kernel32.SetFilePointerEx(
            self.handle,
            ctypes.c_longlong(offset),
            None,
            0)

    def read_bytes(self):
        Display.show_info("Reading MFT")
        # [TODO] COMPLETE THIS WHEN TESTING WORK PROPERLY
        pass    

    def build_display_info(self):
        # Real MFT Size (bytes)
        mft_size = self.ntfs_info.MftValidDataLength
        
        # Round the MFT size to the next highest multiple of RECORD_SIZE
        # so that complete records are read without truncating data
        self.rounded_mft_size = (mft_size + RECORD_SIZE - 1) // RECORD_SIZE * RECORD_SIZE
        
        return {
            "Bytes per cluster" : f"{self.ntfs_info.BytesPerCluster} bytes",
            "MFT LCN" : f"{self.ntfs_info.MftStartLcn} cluster",
            "MFT size": f'{self.rounded_mft_size} bytes',
            "MFT offset" : f"{self.ntfs_info.MftStartLcn * self.ntfs_info.BytesPerCluster} bytes" 
        }

    
