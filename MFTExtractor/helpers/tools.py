import re

class Utils:

    # Validator

    @staticmethod
    def is_correct_volume(volume : str)-> bool:
        er = r"^[A-Z]:?\\?$"
        return bool(re.match(er,volume.strip(),re.IGNORECASE))
    
    def get_volume_letter(volume : str) -> str:
        er = r"^([A-Z])"
        mvalue = re.match(er,volume.strip(),re.IGNORECASE)
        return mvalue.group(1).upper()
    
    def is_correct_file_name(file_name : str) -> bool:
        file_name = file_name.strip()
        base_name = file_name.split(".")[0]
        
        er = r"[A-Za-z_]+"
        return bool(re.fullmatch(er,base_name))
    
    def get_output_file_name(file_name : str) -> str:
        file_name = file_name.strip()
        base_name = file_name.split(".")[0]

        return f"{base_name}.bin" 