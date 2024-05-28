from typing import Union
from fastapi import FastAPI, HTTPException
import joblib

from src import CleaningText, KNNClassification
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

# test model KNN
@app.post("/test-model/")
async def test_model_classification(text: str)-> dict:

    if not text:
        raise HTTPException(status_code=400, detail="text perlu dimasukan")
    
    try:
        # loaded model
        knn_model = joblib.load('knn_classification_model/knn_classification_model.pkl')
        vectorizer = joblib.load('knn_classification_model/tfidf_fit_transform.pkl')

        knn = KNNClassification(knn_model, vectorizer)

        predicted_label, probabilitas = knn.predict_label(text)

        response = {
            'massage' : 'sukses memprediksi label',
            'data' : {
                'label-prediksi': knn.label_to_text(predicted_label),
                'probabilitas': probabilitas
            }
        }

        return response
    
    except Exception as ex:

        response = {
            'massage' : 'error server',
            'error' : ex
        }

        return response