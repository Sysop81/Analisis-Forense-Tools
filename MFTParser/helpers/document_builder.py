from models.parsed_mft_record import ParsedMFTRecord 
from helpers.tools import Utils
from display.dhandler import Display
from openpyxl import Workbook
import pandas as pd
from tqdm import tqdm

class DocumentBuilder:

    _FIELDS = [
        "EntryNumber", "SequenceNumber","MFTReference","ParentMFTReference",
        "NameType","Path","FileNameShort", "FileNameLarge", 
        "IsDirectory","IsHidden","IsSystem","IsReadOnly","ContainsADS","ADSFiles",
        "0x10Creation", "0x10Modification", "0x10MFTModification", "0x10Access",
        "0x30Creation", "0x30Modification", "0x30MFTModification", "0x30Access"
    ]

    def __init__(self, _parsed_record_list : list[ParsedMFTRecord],  _file_name: str, _file_type : str):
        self.file_name = _file_name
        self.file_type = _file_type
        self.file_path = Utils.build_output_path(self.file_name, self.file_type)
        self.parsed_records = _parsed_record_list
        self.progress_bar = tqdm(
            total = len(self.parsed_records),
            desc = f"{Display.print_color_text('Processing output file',Display.YELLOW)}",
            unit="records",
            dynamic_ncols = True,
            colour = "GREEN",
        )

    def build_document(self):
        
        if self.file_type in (".csv", "csv"):
            self.build_csv()
            return
        self.build_xlsx()     

    def build_xlsx(self) -> None:
        wb = Workbook()
        ws = wb.active
        ws.title = "MFT Records"
        ws.append(self._FIELDS)

        for record_data in self.parsed_records:
            ws.append([
                    record_data.entry_number,
                    record_data.sequence_number,
                    record_data.mft_reference,
                    record_data.parent_mft_reference,
                    record_data.name_type,
                    record_data.path,
                    record_data.file_name_short,
                    record_data._file_name_large,
                    record_data.IsDirectory,
                    record_data.IsHidden,
                    record_data.IsSystem,
                    record_data.IsReadOnly,
                    record_data.IsADS,
                    record_data.ADSFiles,
                    record_data._0x10Creation,
                    record_data._0x10Modification,
                    record_data._0x10MFTModification,
                    record_data._0x10Access,
                    record_data._0x30Creation,
                    record_data._0x30Modification,
                    record_data._0x30MFTModification,
                    record_data._0x30Access
                ])
            self.progress_bar.update(1)
            
        self.progress_bar.set_postfix_str(Display.print_color_text("Saving file...",Display.YELLOW), refresh=True)
        wb.save(self.file_path)

        self.close_progress_bar()
    
    def build_csv(self) -> None:
        records = []

        for record in self.parsed_records:
            if record is None:
                continue

            records.append(record.to_dict())
            self.progress_bar.update(1)

        df = pd.DataFrame(records)
        df.to_csv(self.file_path, index=False, encoding="utf-8-sig")
        
        self.close_progress_bar()

    def close_progress_bar(self)-> None:
        self.progress_bar.set_postfix_str(Display.print_color_text("Done",Display.GREEN), refresh=True)
        self.progress_bar.close()
        tqdm.write(
            f"{Display.print_color_text(self.file_type.upper(), Display.RED)} file built: "
            f"{Display.print_color_text(self.file_path, Display.GREY)}"
        )
