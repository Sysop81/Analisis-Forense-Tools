"""
    MFTParser v1.0
    MFTParser - Tool to parse the content of attributes from a binary MFT file to Excel or CSV.
    Author: José Ramón López Guillén
    GitHub: github.com/Sysop81

"""

from display.dhandler import Display
from params.params_handler import Parameters
from parser.mft_parser import MFTParser


def main():
    Display.show_banner()

    params = Parameters()

    #print(f"Bin input: {params.get_input()} file name: {params.get_file_name()} file type: {params.get_file_type()}")
    MFT_RECORD_SIZE = 1024 # TODO MOVE TO CONFIG FILE
       
    mft_parser = MFTParser()
    


    with open(params.get_input(), "rb") as f:
        #entry_number = 0
        while (record := f.read(MFT_RECORD_SIZE)) and len(record) == MFT_RECORD_SIZE:
            if record[0:4] == b"FILE":
                mft_parser.append_record(record)
            #entry_number += 1
            #if entry_number == 100: break

