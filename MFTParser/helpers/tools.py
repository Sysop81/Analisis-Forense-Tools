import re
import os
from datetime import datetime, timedelta

class Utils:

    # Validator

    @staticmethod
    def is_correct_file_name(file_name : str) -> bool:
        file_name = file_name.strip()
        base_name = file_name.split(".")[0]
        
        er = r"[A-Za-z_]+"
        return bool(re.fullmatch(er,base_name))
    
    @staticmethod
    def is_correct_extension(extension : str)-> bool:
        er = r"^\.?(xlsx|csv)$"
        return bool(re.match(er,extension.strip(),re.IGNORECASE))
    
    @staticmethod
    def exist_input_file(inputfile: str):
        return os.path.exists(inputfile)
    
    # Time

    @staticmethod
    def filetime_to_dt(filetime):
        return datetime(1601,1,1) + timedelta(microseconds=filetime//10)
    
    # Strings
    
    @staticmethod
    def clean_string(s):
     return "".join(c if c.isprintable() else "_" for c in s)
    
