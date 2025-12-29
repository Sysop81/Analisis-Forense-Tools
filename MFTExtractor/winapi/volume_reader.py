import ctypes
from ctypes import wintypes
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

    """
        Method close_handle
        This method closes the volume handle.
        Resource. https://learn.microsoft.com/en-us/windows/win32/api/handleapi/nf-handleapi-closehandle
    """
    def close_handle(self):
        kernel32.CloseHandle(self.handle)

    def get_ntfs_info(self):
        Display.show_info(" Getting NTFS information...")
        try:
            self.ntfs_info = get_ntfs_info(self.handle)
            Display.show_ntfs_info(self.build_display_info())
        except OSError as e:
            self.close_handle()
            Display.show_error(e)
            Display.show_end_program(1)                

    """
        Method set_file_pointer
        This method places the pointer at the start of the MFT
        Resource. https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfilepointerex
    """
    def set_file_pointer(self):
        Display.show_info("Moving the pointer to the start of the MFT")
        offset = self.ntfs_info.MftStartLcn * self.ntfs_info.BytesPerCluster # Get offset in bytes to set the cursor
        is_ok = kernel32.SetFilePointerEx(
            self.handle,
            ctypes.c_longlong(offset),
            None,
            0) # FILE_BEGIN
        
        if not is_ok:
            self.close_handle()
            Display.show_error("Failed to move pointer to start of MFT")
            Display.show_end_program(1)

    """
        Method read_bytes
        This method reads the MFT and stores the bytes in a class property "complete_mft_buffer"
        Resource. https://learn.microsoft.com/es-es/windows/win32/api/fileapi/nf-fileapi-readfile
    """
    def read_mft_bytes(self):
        Display.show_info("Reading MFT")
        
        self.complete_mft_buffer = b""                    # buffer to store the bytes read from the MFT
        max_bytes_per_read = RECORD_SIZE * RECORD_SIZE    # 1MB to read bytes in each loop interaction
        rounded_mft_size = self.rounded_mft_size

        while rounded_mft_size > 0:
            # Bytes to read in each loop
            bytes_to_read = min(self.rounded_mft_size,max_bytes_per_read)
            buffer = ctypes.create_string_buffer(bytes_to_read)
            read = wintypes.DWORD()
            
            is_ok = kernel32.ReadFile(
                self.handle,
                buffer,
                bytes_to_read,
                ctypes.byref(read),
                None
            )

            # Checking
            if not is_ok:
                self.close_handle()
                Display.show_error("failed reading MFT")
                Display.show_end_program(1)

            if read.value == 0: break

            # Add reading bytes to the complete buffer & subtract the bytes read from the remaining size
            self.complete_mft_buffer += buffer.raw[:read.value]
            rounded_mft_size -= read.value
        
        self.close_handle()

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

    
