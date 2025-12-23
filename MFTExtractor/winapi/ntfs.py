import ctypes
from ctypes import wintypes

# Windows Access Rights. Need to access in read only mode
GENERIC_READ = 0x80000000

# File Share modes.
# Allows other processes reading & writing the resourse
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002

# Creation Disposition
# Open object only if it exists
# Required when opening volumes & devices
OPEN_EXISTING = 3

# File System Control Codes
# Control code used to get NTFS volume information
FSCTL_GET_NTFS_VOLUME_DATA = 0x00090064

# Value returned by CreateFileW when handle creation fails
INVALID_HANDLE_VALUE = wintypes.HANDLE(-1).value

# Windows DLLs
# Kernel to low level system call "CreateFileW, DeviceIoControl, CloseHandle"
# Shell used for privilege checks
kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
shell32 = ctypes.WinDLL("shell32", use_last_error=True)

# NTFS Struct
# Map the NTFS_VOLUME_DATA_BUFFER returned by FSCTL_GET_NTFS_VOLUME_DATA
# This struct contains metadata about NTFS volume (size, location..)
# Check in https://learn.microsoft.com/sk-sk/windows/win32/api/winioctl/ns-winioctl-ntfs_volume_data_buffer
class NTFS_VOLUME_DATA_BUFFER(ctypes.Structure):
    _fields_ = [
        ("VolumeSerialNumber", wintypes.LARGE_INTEGER),     # Serial number of the volume
        ("NumberSectors", wintypes.LARGE_INTEGER),          # Total number of sectors on the volume
        ("TotalClusters", wintypes.LARGE_INTEGER),          # Total number of clusters "
        ("FreeClusters", wintypes.LARGE_INTEGER),           # Number of free clusters  
        ("TotalReserved", wintypes.LARGE_INTEGER),          # Number of the reserved clusters
        ("BytesPerSector", wintypes.DWORD),                 # Number of bytes per sector
        ("BytesPerCluster", wintypes.DWORD),                # Number of bytes per cluster
        ("BytesPerFileRecordSegment", wintypes.DWORD),      # Number of bytes in each File Record Segment (used in MFT)
        ("ClustersPerFileRecordSegment", wintypes.DWORD),   # Number of clusters per File record Segment
        ("MftValidDataLength", wintypes.LARGE_INTEGER),     # Valid data length of the MFT (bytes)
        ("MftStartLcn", wintypes.LARGE_INTEGER),            # Logical Cluster Number where MFT start
        ("Mft2StartLcn", wintypes.LARGE_INTEGER),           # Logical Cluster Number of the second copy of the MFT (MFT mirror)
        ("MftZoneStart", wintypes.LARGE_INTEGER),           # Start of the MFT zone 
        ("MftZoneEnd", wintypes.LARGE_INTEGER),             # End of the MFT zone
    ]