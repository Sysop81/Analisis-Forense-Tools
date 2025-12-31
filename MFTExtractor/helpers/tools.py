import re
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from display.dhandler import Display

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
        
        # Get hashes & build the manifest file
        hashes = Utils.calculate_hashes(complete_path)
        Utils.build_manifest(hashes,filename,output_path)

    @staticmethod
    def build_manifest(hashes : dict,filename : str,path : Path):
        complete_path = path / f'Manifest_{filename.split(".")[0]}.txt'
        with open(complete_path,"w",encoding="utf-8") as f:
            # Header
            f.write("EVIDENCE INTEGRITY REPORT\n")
            f.write('=' * 80 + '\n')

            # Body. Tool
            f.write("Tool Information\n")
            f.write('-' * 80 + '\n')
            f.write(f"Name: {Display.PROGRAM_NAME}\n")
            f.write(f"Version: {Display.VERSION}\n")
            f.write(f"Source: {Display.GITHUB}\n\n")
            
            # Body. Evidence
            f.write("Evidence Information\n")
            f.write('-' * 80 + '\n')
            f.write(f"File: {path / filename}\n")
            f.write(f"Size: {os.path.getsize(path / filename)} bytes\n")
            f.write(f"Acquisition UTC: {datetime.now(timezone.utc).isoformat()}\n\n")

            # Body. Hashes
            f.write("Hashes\n")
            f.write('-' * 80 + '\n')
            for key, value in hashes.items():
                f.write(f"{key.upper()}: {value}\n")
        

    # Hasher

    @staticmethod
    def calculate_hashes(path : Path)->dict:
        md5 = hashlib.md5()
        sha256 = hashlib.sha256()
        block_size = 4096

        with open(path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                md5.update(block)
                sha256.update(block)
              
        return {
            "md5" : md5.hexdigest(),
            "sha256" : sha256.hexdigest()
         }       
