import argparse
import sys
from helpers.tools import Utils
from display.dhandler import Display

class Parameters:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description=f"Help for {Display.print_color_text('MFTExtractor',Display.YELLOW)}")
        self.add_params()
        self.args = self.parser.parse_args()
        self.validate_params()

    def add_params(self):
        self.parser.add_argument("-i",
                                metavar="<VOL_LETTER>", 
                                default="C",
                                help=f"By default volume {Display.RED}C:{Display.RESET} is used. To change use [{Display.print_color_text('Example:',Display.CYAN)}{Display.GREY} {Display.PROGRAM_NAME} -i <VOL_LETTER>{Display.RESET}]"
        )
        self.parser.add_argument("-o",
                                metavar="<NEW_NAME.bin>", 
                                default="MFT.bin",
                                help=f"Output file. To change default name use [{Display.print_color_text('Example:',Display.CYAN)} {Display.GREY} {Display.PROGRAM_NAME} -o <new_name.bin>{Display.RESET}]"
        )       

    def get_params(self) -> dict:
         return {
             "input"  : Utils.get_volume_letter(self.args.i),
             "output" : Utils.get_output_file_name(self.args.o) 
         }
    
    def get_command_line_args(self):
        return " ".join(sys.argv)

    def validate_params(self):
        
        if not Utils.is_correct_volume(self.args.i):
            Display.show_error(f" Wrong input NTFS volume letter.{Display.GREY} Use [-h] to show help.{Display.RESET}")
            Display.show_end_program(1)

        if not Utils.is_correct_file_name(self.args.o):
            Display.show_error(f" Wrong output the file name. {Display.GREY}Only letters, the symbol \"_\" and THE \".bin\" extension are allowed{Display.RESET}")
            Display.show_end_program(1)