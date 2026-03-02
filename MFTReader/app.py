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
        
        # Builds attrs    
        mft_reader.build_record_struct()
        mft_reader.build_standard_info() 
        mft_reader.build_file_name_info()
        mft_reader.build_data_info()
        mft_reader.build_general_info()
        #mft_reader.build_ads_files() # TODO complete this
        mft_reader.build_file_flags()
        
        # Displays
        Display.show_structure_table(mft_reader.record_structure_list) # record structure info
        Display.show_general_info_table(mft_reader.get_general_info())
        Display.show_flags(mft_reader.get_file_flags())
        Display.show_standard_info_table(mft_reader.get_standard_info())
        Display.show_file_info_table(mft_reader.get_filename_info())

        #Display.show_data_ads_info_table(mft_reader.get_ads_info())