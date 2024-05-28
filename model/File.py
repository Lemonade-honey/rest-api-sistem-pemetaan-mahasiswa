from typing import List
from pydantic import BaseModel

class File(BaseModel):
    
    # files, berisi List data string
    files: List[str]