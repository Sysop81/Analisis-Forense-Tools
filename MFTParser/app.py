"""
    MFTParser v1.0
    MFTParser - Tool to parse the content of attributes from a binary MFT file to Excel or CSV.
    Author: José Ramón López Guillén
    GitHub: github.com/Sysop81

"""
from tqdm import tqdm
from pathlib import Path
from display.dhandler import Display
from params.params_handler import Parameters
from parser.mft_parser import MFTParser
from helpers.document_builder import DocumentBuilder

def main():
    Display.show_banner()
    params = Parameters()

    # Parsing records 
    Display.show_info(" MFT parsing started") 
    MFT_RECORD_SIZE = 1024
    MFT_SIZE = (Path(params.get_input())).stat().st_size
    mft_parser = MFTParser()
    with open(params.get_input(), "rb") as f:
        entry_number = 0
        progress_bar = tqdm(
            total = MFT_SIZE,
            desc = f"{Display.print_color_text('Processing MFT',Display.YELLOW)}",
            unit="B",
            unit_scale=True,
            dynamic_ncols = True,
            colour = "GREEN"
        )  
        while (record := f.read(MFT_RECORD_SIZE)) and len(record) == MFT_RECORD_SIZE:
            
            try:
                mft_parser.append_record(record,entry_number)
            except:
                pass
            progress_bar.update(MFT_RECORD_SIZE)
            entry_number += 1
        progress_bar.set_postfix_str(Display.print_color_text("Done",Display.GREEN), refresh=True)    
        progress_bar.close()

    Display.show_info(" Building parent directories")        
    mft_parser.build_paths()
    parsed_records = mft_parser.parsed_record_list
    
    # Build documents
    Display.show_info(" Building output document")
    dBuilder = DocumentBuilder(
        parsed_records,
        params.get_file_name(),
        params.get_file_type()
    )

    dBuilder.build_document()
    
    Display.show_end_program()
