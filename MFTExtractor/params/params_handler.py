import argparse
from helpers.tools import Utils

class Parameters:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="Help for MFTExtractor")
        self.add_params()
        self.args = self.parser.parse_args()
        self.validate_params()

    def add_params(self):
        self.parser.add_argument("-i",
                                metavar="<VOL_LETTER>", 
                                default="C",
                                help="By default volume C: is used. To change use [Example: -i <VOL_LETTER>]"
        )
        self.parser.add_argument("-o",
                                metavar="<NEW_NAME.bin>", 
                                default="MFT.bin",
                                help="Output file. To change default name use [Example: -o <new_name.bin>]"
        )       

    def get_params(self) -> dict:
         return {
             "input"  : Utils.get_volume_letter(self.args.i),
             "output" : Utils.get_output_file_name(self.args.o) 
         }

    def validate_params(self):
        
        if not Utils.is_correct_volume(self.args.i):
            print("Error with input NTFS volume letter. Use [-h] to show help")
            exit(1) 

        if not Utils.is_correct_file_name(self.args.o):
            print("Error entering the file name. Only letters, the symbol \"_\" and THE \".bin\" extension are allowed")
            exit(1)  