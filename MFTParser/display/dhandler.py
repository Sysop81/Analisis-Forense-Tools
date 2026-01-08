import pyfiglet
from colorama import init, Fore, Style

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
    PROGRAM_NAME = "MFTParser"
    VERSION = "1.0"
    AUTHOR = "Jose Ramon Lopez Guillen"
    GITHUB = "github.com/Sysop81"
    DESCRIPTION = f"{PROGRAM_NAME} - Tool to parse the content of attributes from a binary MFT file to Excel or CSV."

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
    def show_end_program(code : int = 0):
        msg = f"{Display.GREEN} Program finished successfully{Display.RESET}"    
        if code != 0:
            msg =  f"{Display.RED} Program finished with errors{Display.RESET}" 

        print(f"{Display.CYAN}[Info]{Display.RESET}{msg}")
        exit(code)    
