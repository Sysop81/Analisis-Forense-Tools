import pyfiglet
import os
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

    UPPER_LEFT = '\u250c'
    UPPER_RIGHT = '\u2510'
    LOWER_LEFT = '\u2514'
    LOWER_RIGTH = '\u2518'
    HORIZONTAL = '\u2500'
    VERTICAL = '\u2502'
    CROSS_LEFT = '\u251c'
    CROSS_RIGTH = '\u2524'
    CROSS = '\u253c'
    T_HORIZONTAL_DOWN = '\u252c'
    T_HORIZONTAL_UP = '\u2534'

    TOTAL_SIZE = 80
    TITLE_SIZE = 25        

    @staticmethod
    def show_banner(launch_init : bool = True):
        if launch_init : init()
        print(f"{Display.GREEN}{(pyfiglet.figlet_format(Display.PROGRAM_NAME, font="doom")).strip()}{Display.RESET}")
        Display.show_description()

    @staticmethod
    def show_description():
        print(Display.print_color_text(f"Version: {Display.VERSION}",Display.GREEN))
        print(Display.print_color_text(f"Author : {Display.AUTHOR}",Display.GREY))
        print(Display.print_color_text(f"GitHub : {Display.GITHUB}",Display.GREY))
        print(Display.print_color_text(f"{Display.DESCRIPTION}\n",Display.GREY))

    @staticmethod
    def show_options_menu(show_banners : bool = True) -> str: 
        
        if show_banners: Display.show_banner(False)

        print(f"{Display.YELLOW}MFTReader options menu{Display.RESET}")
        print(f"\t{Display.GREEN}1.{Display.RESET} {Display.GREY}Show Record Structure.{Display.RESET}")
        print(f"\t{Display.GREEN}2.{Display.RESET} {Display.GREY}Show General Information.{Display.RESET}")   
        print(f"\t{Display.GREEN}3.{Display.RESET} {Display.GREY}Show Standard Information.{Display.RESET}")  
        print(f"\t{Display.GREEN}4.{Display.RESET} {Display.GREY}Show File Name Information.{Display.RESET}")   
        print(f"\t{Display.GREEN}5.{Display.RESET} {Display.GREY}Show Data Information.{Display.RESET}")
        print(f"\t{Display.GREY}6.{Display.RESET} {Display.RED}Exit.{Display.RESET}")   

        return input("Please, select an option: ") 
    
    @staticmethod
    def show_user_action():
        input(f"{Display.GREY}Press{Display.RESET} {Display.RED}ENTER{Display.RESET}{Display.GREY} to continue{Display.RESET}")
        os.system('cls' if os.name == 'nt' else 'clear')

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
        
        # Title
        Display.build_table_title("MFT Record structure")
        
        # Header
        clean_header = Display.build_table_header({
           'ATTRIBUTE':24,
           'TYPE':15,
           'START':4,
           'END':9,
           'LENGTH':15 
        })
        
        # body
        left : str = Display.CROSS_LEFT
        rigth : str = Display.CROSS_RIGTH
        parent_horizontal = Display.CROSS
        for index, record in enumerate(mftrecord_list):
            print(f"\t{Display.VERTICAL}{Display.GREY}{record._attr:<25}{Display.RESET}" 
                  f"{Display.VERTICAL} {record._type:<15} "
                  f"{Display.VERTICAL} {record._start_offset:<5} "
                  f"{Display.VERTICAL} {(record._start_offset + record._length - 1):<10}"
                  f"{Display.VERTICAL} {f"{record._length} bytes":<14} {Display.VERTICAL}"
            )

            Display.build_table_row_line(
                index=index,
                total=len(mftrecord_list),
                left=left,
                rigth=rigth,
                clean_header=clean_header,
                parent_horizontal=parent_horizontal
            )   

    @staticmethod
    def show_default_info_table(g_info : dict, title : str = "INFO") -> None:
        # Title
        Display.build_table_title(title)
        
        # Header
        clean_header = Display.build_table_header({
            'ATTRIBUTE' : 24,
            'DATA' : 53
        })
        
        # body
        Display.build_table_body(g_info,clean_header)

    @staticmethod
    def build_table_body(data : dict,clean_header : str)->None:
        
        # body
        left : str = Display.CROSS_LEFT
        rigth : str = Display.CROSS_RIGTH
        parent_horizontal = Display.CROSS
        formatted_value : str
        for index, (key,value) in enumerate(data.items()):
            # TODO REFACT THIS
            value = str(value)
            value = value.replace("\n", "").replace("\r", "")
            if value == 'False':
                formatted_value = f"{Display.RED}{value:<52}{Display.RESET}"
            elif value == 'True':
                formatted_value = f"{Display.GREEN}{value:<52}{Display.RESET}"
            else:
                formatted_value =  f"{value:<52}"
            max_len = 52
            if len(value) > max_len:
                chunks = [value[i:i+max_len] for i in range(0, len(value), max_len)]
                for i, val in enumerate(chunks):
                    if i == 0:
                        print(f"\t{Display.VERTICAL}{Display.GREY}{key:<25}{Display.RESET}" 
                        f"{Display.VERTICAL} {val:<52} {Display.VERTICAL}")
                    else:
                        print(f"\t{Display.VERTICAL}{Display.GREY}{'':<25}{Display.RESET}" 
                                                f"{Display.VERTICAL} {val:<52} {Display.VERTICAL}")
            else:
                print(f"\t{Display.VERTICAL}{Display.GREY}{key:<25}{Display.RESET}" 
                    f"{Display.VERTICAL} {formatted_value} {Display.VERTICAL}"
                )

            Display.build_table_row_line(
                index=index,
                total=len(data),
                left=left,
                rigth=rigth,
                clean_header=clean_header,
                parent_horizontal=parent_horizontal
            )
    
    @staticmethod
    def build_table_header(attributes : dict)->str:
        clean_header : str = f"\t{Display.VERTICAL}"
        header : str = f"\t{Display.VERTICAL}"

        for index,(attr, width) in enumerate(attributes.items()):
            clean_header += f"{attr:<{width}} {Display.VERTICAL} "
            if index < len(attributes.items()) - 1:
                header += f"{Display.YELLOW}{attr:<{width}}{Display.RESET} {Display.VERTICAL} "
            else:
                header += f"{Display.YELLOW}{attr:<{width}}{Display.RESET}{Display.VERTICAL}"    
        clean_header += Display.VERTICAL
        
        print(f"\t{Display.build_separator(int(Display.TOTAL_SIZE),Display.HORIZONTAL,Display.CROSS_LEFT,Display.UPPER_RIGHT,clean_header,Display.T_HORIZONTAL_DOWN,True)}")
        print(header)
        print(f"\t{Display.build_separator(
            Display.TOTAL_SIZE,
            Display.HORIZONTAL,
            Display.CROSS_LEFT,
            Display.CROSS_RIGTH,
            clean_header)}"
        )

        return clean_header

    @staticmethod
    def build_table_title(title : str):
        print(f"\n\t{Display.build_separator(Display.TITLE_SIZE,Display.HORIZONTAL,Display.UPPER_LEFT,Display.UPPER_RIGHT)}")
        print(f"\t{Display.VERTICAL} {title} {(Display.TITLE_SIZE - len(title)-3)*" "} {Display.VERTICAL}")

    @staticmethod
    def build_table_row_line(index: int, total: int,left:str, rigth : str,clean_header : str,parent_horizontal : str):
        if index >= total - 1:
                left = Display.LOWER_LEFT
                rigth = Display.LOWER_RIGTH
                parent_horizontal = Display.T_HORIZONTAL_UP

        print(f"\t{Display.build_separator(int(Display.TOTAL_SIZE),Display.HORIZONTAL,left,rigth,clean_header,parent_horizontal)}")

    @staticmethod
    def build_separator(value : int, separator : str, start : str,end : str, parent_text : str = "",parent_separator : str = '\u253c',is_title : bool = False)-> str:
        CROSS = '\u253c'
        VERTICAL = '\u2502'
        NUM_SPACES = 2
        response = separator * value
        counter : int = 0
        if parent_text:
            text_list = list(parent_text)
            response_list = list(response)
            for index,character in enumerate(text_list):
               if character == VERTICAL and index > 1 and index <= value:
                   if is_title and counter == 0:
                       response_list[index - NUM_SPACES] = CROSS
                   else : response_list[index - NUM_SPACES] = parent_separator
                   counter += 1   
            response = "".join(response_list)
            
        return f"{start}{response}{end}"    