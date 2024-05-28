from typing import Union
from fastapi import FastAPI

from src import CleaningText

app = FastAPI()

# Index Root Project
@app.get("/")
def index_root()-> dict:

    response = {
        'server' : 'success connect',
        'status' : 200
    }

    return response