"""
MFTExtractor v1.0
MFTExtractor - Tool for reading and extracting the Master File Table (MFT) in an NTFS file system.
Author: José Ramón López Guillén
GitHub: github.com/Sysop81

"""

from display.dhandler import Display
from params.params_handler import Parameters


def main():
    Display.show_banner()
    params = Parameters() 
    
    print(params.get_params())

    Display.show_info("End program")    