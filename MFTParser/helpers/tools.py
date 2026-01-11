import re
import os
from datetime import datetime, timedelta
from pathlib import Path

class Utils:

    # Validator

    NON_PRINTABLE_RE = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]')
    ALLOWED_CHARS_RE = re.compile(r'[^a-zA-Z0-9 _\.\-\\]')

    @staticmethod
    def has_non_printable_chars(text):
        if not isinstance(text, str):
            return False
        return bool(Utils.NON_PRINTABLE_RE.search(text))

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
    
    # Folders

    @staticmethod
    def build_output_path(file_name : str, file_type : str) -> Path:
        output_folder = "output"
        output_path = Path(__file__).resolve().parents[1] / output_folder
        output_path.mkdir(parents=True, exist_ok=True)
        
        if not file_type.startswith("."):
            file_type = f".{file_type}"
        
        return output_path / f"{file_name}{file_type}"
    
