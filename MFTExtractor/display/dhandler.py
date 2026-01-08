import pyfiglet
from colorama import init, Fore, Style

class Display:
     # Basic colors
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
    PROGRAM_NAME = "MFTExtractor"
    VERSION = "1.0"
    AUTHOR = "Jose Ramon Lopez Guillen"
    GITHUB = "github.com/Sysop81"
    DESCRIPTION = f"{PROGRAM_NAME} - Tool to extract the $MFT from an NTFS file system."

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
    def print_color_text(text, color):
        return f"{color}{text}{Display.RESET}"

    @staticmethod
    def show_input_question(text,color = None) -> bool:
        if color == None : color = Display.GREY
        question = (f"{Display.print_color_text(text,color)}"
                   f" [{Display.print_color_text("Y",Display.GREEN)}es] or [{Display.print_color_text("N",Display.RED)}o]") 
        
        while True:
            res = input(question)
            if res.lower() in ("yes","y"):
                return True
            elif res.lower() in("no","n"):
                Display.show_info(F"Remember. To run {Display.print_color_text(Display.PROGRAM_NAME,Display.YELLOW)} you must launch it in a console with administrator privileges.")
                return False
            else:
                question = f"Please type {Display.print_color_text("Y",Display.GREEN)}es or {Display.print_color_text("N",Display.RED)}o."
    
    @staticmethod
    def get_user_answer() -> bool:
        Display.show_warning(f"{Display.PROGRAM_NAME} requires administrator privileges.")
        return Display.show_input_question("Do you want to run the program with administrator privileges?")

    @staticmethod
    def show_end_program(code : int = 0):
        msg = f"{Display.GREEN} Program finished successfully{Display.RESET}"    
        if code != 0:
            msg =  f"{Display.RED} Program finished with errors{Display.RESET}" 

        print(f"{Display.CYAN}[Info]{Display.RESET}{msg}")
        exit(code)

    @staticmethod
    def show_ntfs_info(ntfs_info : dict):
        
        max_key_length =  max(len(key) for key in ntfs_info.keys())
        max_value_length =  max(len(str(value)) for value in ntfs_info.values())
        total = (max_key_length + max_value_length) + 5
        
        UPPER_LEFT = '\u250c'
        UPPER_RIGHT = '\u2510'
        LOWER_LEFT = '\u2514'
        LOWER_RIGTH = '\u2518'
        HORIZONTAL = '\u2500'
        VERTICAL = '|'

        # Header
        print(f"\n\t{Display.build_separator(total,HORIZONTAL,UPPER_LEFT,UPPER_RIGHT)}")
        print("\t|{:<{}} | {:<{}}|".format("Metadata", max_key_length, "Values", (max_value_length + 2)))
        print(f"\t{Display.build_separator(total,HORIZONTAL,VERTICAL,VERTICAL)}")

        # Body
        for index,(key,value) in enumerate(ntfs_info.items()):
            print(f"\t|{Display.print_color_text(key,Display.YELLOW)} | {Display.print_color_text(Display.build_mft_values(value,max_value_length),Display.GREY)} |")
             
            if index < len(ntfs_info) - 1:
                print(f"\t{Display.build_separator(total,HORIZONTAL,VERTICAL,VERTICAL)}")
        # Footer    
        print(f"\t{Display.build_separator(total,HORIZONTAL,LOWER_LEFT,LOWER_RIGTH)}\n")            
                 

    @staticmethod
    def build_separator(value : int, separator : str,start : str,end : str)-> str:
        return f"{start}{separator * value}{end}"        

    @staticmethod
    def build_mft_values(values : list, max_length : int):
       str_value = str(values)
       diff = max_length - (len(str_value) - 1)
       
       return str_value + (" " * diff)           
