"""
    MFTParser v1.0
    MFTParser - Tool to parse the content of attributes from a binary MFT file to Excel or CSV.
    Author: José Ramón López Guillén
    GitHub: github.com/Sysop81

"""

from display.dhandler import Display
from params.params_handler import Parameters
from parser.mft_parser import MFTParser
from helpers.document_builder import DocumentBuilder

def main():
    Display.show_banner()
    params = Parameters()

    # Parsing records 
    Display.show_info("Parsing MFT")   
    MFT_RECORD_SIZE = 1024
    mft_parser = MFTParser()
    with open(params.get_input(), "rb") as f:
        entry_number = 0
        while (record := f.read(MFT_RECORD_SIZE)) and len(record) == MFT_RECORD_SIZE:
            
            try:
                mft_parser.append_record(record,entry_number)
            except:
                pass
            entry_number += 1
            
    mft_parser.build_paths()
    parsed_records = mft_parser.parsed_record_list
    
    # Build documents
    Display.show_info("Build documents")
    dBuilder = DocumentBuilder(
        parsed_records,
        params.get_file_name(),
        params.get_file_type()
    )

    dBuilder.build_document()
    
    Display.show_end_program()
