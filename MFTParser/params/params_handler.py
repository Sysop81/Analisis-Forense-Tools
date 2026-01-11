import argparse
from helpers.tools import Utils
from display.dhandler import Display

class Parameters:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=f"Help for {Display.print_color_text('MFTParser',Display.YELLOW)}",
            formatter_class= argparse.RawTextHelpFormatter
        )
        self.add_params()
        self.args = self.parser.parse_args()
        self.validate_params()

    def get_input(self):
        return self.input
    
    def get_file_name(self):
        return self.filename
    
    def get_file_type(self):
        return self.filetype
    
    def add_params(self):
        self.parser.add_argument("-i",
                                metavar="<MFT.bin>", 
                                default="MFT.bin",
                                help=f"By default {Display.RED}MFT.bin{Display.RESET} is used. To change use [{Display.print_color_text('Example:',Display.CYAN)}{Display.GREY} {Display.PROGRAM_NAME} -i <new_name.bin>{Display.RESET}]"
        )
        self.parser.add_argument("-filename",
                                metavar="<FILE_NAME>", 
                                default="MFT_parser",
                                help=f"Output file name. To change use [{Display.print_color_text('Example:',Display.CYAN)} {Display.GREY} {Display.PROGRAM_NAME} -filename <new_name>{Display.RESET}]"
        ) 
        self.parser.add_argument("-filetype",
                                metavar="<FILE_TYPE>", 
                                default="xlsx",
                                help=(f"Output file type. To change use [{Display.print_color_text('Example:',Display.CYAN)} {Display.GREY} {Display.PROGRAM_NAME} -filetype <type>{Display.RESET}]\n"
                                     f"[{Display.GREEN}Allowed types:{Display.RESET} {Display.GREEN}CSV, XLSX{Display.RESET}]"
                                )     
        ) 

    def validate_params(self):

        if not Utils.exist_input_file(self.args.i):
            Display.show_error(f" Wrong input file. {Display.GREY} The {self.args.i} does not exist {Display.RESET}")
            Display.show_end_program(1)
        
        if not Utils.is_correct_file_name(self.args.filename):
            Display.show_error(f" Wrong output file name. {Display.GREY}Only letters and the symbol \"_\" are allowed{Display.RESET}")
            Display.show_end_program(1)

        if not Utils.is_correct_extension(self.args.filetype):
            Display.show_error(f" Wrong file type. {Display.GREY}Only \"CSV or XLSX\" are allowed{Display.RESET}")
            Display.show_end_program(1)

        self.build_params()    

    def build_params(self):
        self.input  = self.args.i
        self.filename = self.args.filename
        self.filetype = self.args.filetype  