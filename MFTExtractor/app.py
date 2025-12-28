"""
MFTExtractor v1.0
MFTExtractor - Tool for reading and extracting the Master File Table (MFT) in an NTFS file system.
Author: José Ramón López Guillén
GitHub: github.com/Sysop81

"""

from display.dhandler import Display
from params.params_handler import Parameters
from helpers.privileges import Privileges
from winapi.volume_reader import VolumeReader

def main():
    Display.show_banner()
    # Get params and check admin privileges
    params = Parameters() 
    Privileges.check_privileges(params.get_command_line_args())    

    # Handle NTFS vol
    ntfs_volume = VolumeReader(params.get_input())
    ntfs_volume.get_ntfs_info()
    ntfs_volume.set_file_pointer()
    
    Display.show_info("End program")    