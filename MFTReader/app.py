"""
    MFTReader v1.0
    MFTReader - Tool to display the content of the attributes of a record stored in the MFT.
    Author: José Ramón López Guillén
    GitHub: github.com/Sysop81

"""
import os
from display.dhandler import Display
from params.params_handler import Parameters
from reader.mft_reader import MFTReader

def main():
    Display.show_banner()
    params = Parameters()

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
        mft_reader.build_file_flags()

        # MENU. TODO REFACT THIS
        _exit : bool = False
        _show_banners : bool = False
        while not _exit:
            
            user_entry =  Display.show_options_menu(_show_banners)
            msg : str = ''
            is_error : bool = False
            try:
                user_entry = int(user_entry)
                if user_entry <= 0 or user_entry >= 7:
                    msg = "Error. Invalid option selected."
                    is_error = True 
            except ValueError:
                msg = "Error, Invalid input detected. Only numbers [1-6]"
                is_error = True 
            
            if is_error:
                Display.show_error(msg)
            else:
                match user_entry:
                    case 1:
                        # Record MFT Structure
                        Display.show_structure_table(mft_reader.record_structure_list)
                    case 2:
                        # General Record information && Flags
                        Display.show_default_info_table(mft_reader.get_general_info(),"GENERAL_INFORMATION")
                        Display.show_default_info_table(mft_reader.get_file_flags(),"FILE FLAGS")
                    case 3:
                        # Standard Information
                        Display.show_default_info_table(mft_reader.get_standard_info(),"STANDARD_INFORMATION")
                    case 4:
                        # File Name Information
                        fn_list = mft_reader.file_name_attr_list
                        for fn_info in fn_list:
                            Display.show_default_info_table(fn_info.to_dict(),"FILE_NAME")
                    case 5:
                        # Data Information
                        data_list = mft_reader.data_attr_list
                        for data_info in data_list:
                            Display.show_default_info_table(data_info.to_dict(),"DATA_INFORMATION")
                    case 6:
                        Display.show_end_program()
                        _exit = True
            
            if not _exit:
                if not _show_banners : _show_banners = True
                Display.show_user_action()
        
        