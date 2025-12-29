import re
from pathlib import Path

class Utils:

    # Validator

    @staticmethod
    def is_correct_volume(volume : str)-> bool:
        er = r"^[A-Z]:?\\?$"
        return bool(re.match(er,volume.strip(),re.IGNORECASE))
    
    @staticmethod
    def get_volume_letter(volume : str) -> str:
        er = r"^([A-Z])"
        mvalue = re.match(er,volume.strip(),re.IGNORECASE)
        return mvalue.group(1).upper()
    
    @staticmethod
    def is_correct_file_name(file_name : str) -> bool:
        file_name = file_name.strip()
        base_name = file_name.split(".")[0]
        
        er = r"[A-Za-z_]+"
        return bool(re.fullmatch(er,base_name))
    
    @staticmethod
    def get_output_file_name(file_name : str) -> str:
        file_name = file_name.strip()
        base_name = file_name.split(".")[0]

        return f"{base_name}.bin" 
    
    # FileWriter

    @staticmethod
    def build_output_file(filename : str, mft_data : bytes):
        output_folder = "output"
        output_path = Path(__file__).resolve().parents[1] / output_folder
        output_path.mkdir(parents=True, exist_ok=True)
        complete_path = output_path / filename

        with open(complete_path, "wb") as f:
            f.write(mft_data)
