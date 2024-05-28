from typing import Union
from fastapi import FastAPI, HTTPException

from src import CleaningText
from model import File
from request import ValidateType

app = FastAPI()

# Index Root Project
@app.get("/")
def index_root()-> dict:

    response = {
        'server' : 'success connect',
        'status' : 200
    }

    return response

# route upload file
@app.post("/upload-file/")
async def upload_files(list_file: File)-> dict:

    if not list_file.files:
        raise HTTPException(status_code=400, detail="No files provided")

    # validasi
    ValidateType(['.pdf']).validate_datas(list_file.files)
    
    response = {
        'massage' : 'File berhasil diterima',
        'data': list_file.files
    }

    return response