from typing import List
from fastapi import HTTPException


class ValidateType:

    def __init__(self, type:list) -> None:
        self.file_valid_type = type

    def is_valid_type(self, filename: str) -> bool:
        return any(filename.endswith(ext) for ext in self.file_valid_type)
    
    # validasi file berdasarkan tipe pada list parameter class
    def validate_datas(self, files: List[str]):
        invalid_files = [file for file in files if not self.is_valid_type(file)]
        if invalid_files:
            print(f"Invalid file types: {', '.join(invalid_files)}")
            raise HTTPException(status_code=400, detail=f"Invalid file types: {', '.join(invalid_files)}")