import pyfiglet

class Display:
     # Basic colors
    RED = "\033[31m"
    GREEN = "\033[32m"
    GREY = "\033[90m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[97m"
    RESET = "\033[0m"

    # Program info
    PROGRAM_NAME = "MFTExtractor"
    VERSION = "1.0"
    AUTHOR = "Jose Ramon Lopez Guillen"
    GITHUB = "github.com/Sysop81"
    DESCRIPTION = f"{PROGRAM_NAME} - Tool to extract the $MFT from an NTFS file system."

    @staticmethod
    def show_banner():
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
        print(f"{Display.RED}End program{Display.RESET}")
        exit(code)

    @staticmethod
    def show_ntfs_info(ntfs_info : dict):
        for key,value in ntfs_info.items():
            print(f"{Display.print_color_text(key,Display.YELLOW)}: {Display.print_color_text(value,Display.GREY)}")    
