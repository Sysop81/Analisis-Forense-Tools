"""
    MFTReader v1.0
    MFTReader - Tool to display the content of the attributes of a record stored in the MFT.
    Author: José Ramón López Guillén
    GitHub: github.com/Sysop81

"""

from display.dhandler import Display
from params.params_handler import Parameters
from reader.mft_reader import MFTReader

def main():
    Display.show_banner()
    params = Parameters()

    #print(f"input: {params.get_input()}, entry_number : {params.get_entry_number()}")

    MFT_RECORD_SIZE = 1024
    with open(params.get_input(), "rb") as f:
        # Set cursor in the offset record [entry point] and get the target MFT record
        f.seek(int(params.get_entry_number()) * MFT_RECORD_SIZE)
        record : bytearray = bytearray(f.read(MFT_RECORD_SIZE))

        # Instantiate a mftparser object
        mft_reader = MFTReader(
            params.get_entry_number(),
            record
        )
        
        # build (& SHOW) record structure info    
        mft_reader.build_record_struct()
        Display.show_structure_table(mft_reader.record_structure_list) # [TODO] CHECK -struture param to build and show
        
        #mft_reader.build_attributes()

