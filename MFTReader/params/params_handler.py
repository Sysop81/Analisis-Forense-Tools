import argparse
from helpers.tools import Utils
from display.dhandler import Display

class Parameters:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=f"Help for {Display.print_color_text('MFTReader',Display.YELLOW)}",
            formatter_class= argparse.RawTextHelpFormatter
        )
        self.add_params()
        self.args = self.parser.parse_args()
        self.validate_params()

    def get_input(self):
        return self.input
    
    def get_entry_number(self):
        return self.entry_number
    
    def add_params(self):
        self.parser.add_argument("-i",
                                metavar="<MFT.bin>", 
                                default="MFT.bin",
                                help=f"By default {Display.RED}MFT.bin{Display.RESET} is used. To change use [{Display.print_color_text('Example:',Display.CYAN)}{Display.GREY} {Display.PROGRAM_NAME} -i <new_name.bin>{Display.RESET}]"
        )
        self.parser.add_argument("-entrynumber",
                                metavar="<ENTRY_NUMBER>", 
                                help=f"Entry number of the MFT record to get attributes.[{Display.print_color_text('Example:',Display.CYAN)} {Display.GREY} {Display.PROGRAM_NAME} -entrynumber <parsed_record_entry_number>{Display.RESET}]"
        ) 
        
    def validate_params(self):

        if not Utils.exist_input_file(self.args.i):
            Display.show_error(f" Wrong input file. {Display.GREY} The {self.args.i} does not exist {Display.RESET}")
            Display.show_end_program(1)
        
        if not self.args.entrynumber or not Utils.is_numeric_entry_number(self.args.entrynumber):
            Display.show_error(f" {"Empty" if not self.args.entrynumber else "Wrong"} entry number." 
                               f"{Display.GREY} Only numbers are allowed [0-9]{Display.RESET}")
            Display.show_end_program(1)

        self.build_params()    

    def build_params(self):
        self.input  = self.args.i
        self.entry_number = self.args.entrynumber 