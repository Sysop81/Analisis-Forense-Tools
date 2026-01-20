import pyfiglet
from colorama import init, Fore, Style
from models.mft_record_struct import MFTRecordStruct

class Display:

    RED = Fore.RED
    GREEN = Fore.GREEN
    GREY = Fore.LIGHTBLACK_EX
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    RESET = Style.RESET_ALL
    

    # Program info
    PROGRAM_NAME = "MFTReader"
    VERSION = "1.0"
    AUTHOR = "Jose Ramon Lopez Guillen"
    GITHUB = "github.com/Sysop81"
    DESCRIPTION = f"{PROGRAM_NAME} - Tool to display the content of the attributes of a record stored in the MFT.."

    @staticmethod
    def show_banner():
        init()
        print(f"{Display.GREEN}{(pyfiglet.figlet_format(Display.PROGRAM_NAME, font="doom")).strip()}{Display.RESET}")
        Display.show_description()

    @staticmethod
    def show_description():
        print(Display.print_color_text(f"Version: {Display.VERSION}",Display.GREEN))
        print(Display.print_color_text(f"Author : {Display.AUTHOR}",Display.GREY))
        print(Display.print_color_text(f"GitHub : {Display.GITHUB}",Display.GREY))
        print(Display.print_color_text(f"{Display.DESCRIPTION}\n",Display.GREY))

    @staticmethod
    def show_info(text):
        print(f"{Display.CYAN}[Info]{Display.RESET}{text}")

    @staticmethod
    def show_warning(text):
        print(f"{Display.YELLOW}[Warning]{Display.RESET}{text}")
    
    @staticmethod
    def show_error(text):
        print(f"{Display.RED}[Error]{Display.RESET}{text}")         

    @staticmethod
    def show_text(text : str):
        print(text)
    
    @staticmethod
    def print_color_text(text, color):
        return f"{color}{text}{Display.RESET}"

    @staticmethod
    def show_end_program(code : int = 0):
        msg = f"{Display.GREEN} Program finished successfully{Display.RESET}"    
        if code != 0:
            msg =  f"{Display.RED} Program finished with errors{Display.RESET}" 

        print(f"{Display.CYAN}[Info]{Display.RESET}{msg}")
        exit(code)

    @staticmethod
    def show_structure_table(mftrecord_list : list[MFTRecordStruct])-> None:
        UPPER_LEFT = '\u250c'
        UPPER_RIGHT = '\u2510'
        LOWER_LEFT = '\u2514'
        LOWER_RIGTH = '\u2518'
        HORIZONTAL = '\u2500'
        VERTICAL = '\u2502'
        CROSS_LEFT = '\u251c'
        CROSS_RIGTH = '\u2524'

        TOTAL_SIZE = 80
        TITLE = "MFT Record structure"
        TITLE_SIZE = 25

        # Header
        print(f"\n\t{Display.build_separator(TITLE_SIZE,HORIZONTAL,UPPER_LEFT,UPPER_RIGHT)}")
        print(f"\t{VERTICAL} {TITLE} {(TITLE_SIZE - len(TITLE)-3)*" "} {VERTICAL}")
        print(f"\t{Display.build_separator(int(TOTAL_SIZE),HORIZONTAL,CROSS_LEFT,UPPER_RIGHT)}")
        
        print (
            f"\t{VERTICAL}{Display.YELLOW}{'ATTRIBUTE':<24}{Display.RESET} {VERTICAL} "
            f"{Display.YELLOW}{'TYPE':<15}{Display.RESET} {VERTICAL} "
            f"{Display.YELLOW}{'START':<4}{Display.RESET} {VERTICAL} "
            f"{Display.YELLOW}{'END':<9}{Display.RESET} {VERTICAL} "
            f"{Display.YELLOW}{'LENGTH':<15}{Display.RESET}{VERTICAL}"
        )
        print(f"\t{Display.build_separator(TOTAL_SIZE,HORIZONTAL,VERTICAL,VERTICAL)}")


        # body
        left : str = CROSS_LEFT
        rigth : str = CROSS_RIGTH
        for index, record in enumerate(mftrecord_list):
            print(f"\t{VERTICAL}{Display.GREY}{record._attr:<25}{Display.RESET}" 
                  f"{VERTICAL} {record._type:<15} "
                  f"{VERTICAL} {record._start_offset:<5} "
                  f"{VERTICAL} {(record._start_offset + record._length - 1):<10}"
                  f"{VERTICAL} {f"{record._length} bytes":<14} {VERTICAL}"
            )
            
            if index >= len(mftrecord_list) - 1:
                left = LOWER_LEFT
                rigth = LOWER_RIGTH

            print(f"\t{Display.build_separator(int(TOTAL_SIZE),HORIZONTAL,left,rigth)}")   


    @staticmethod
    def build_separator(value : int, separator : str, start : str,end : str)-> str:
        return f"{start}{separator * value}{end}"     
