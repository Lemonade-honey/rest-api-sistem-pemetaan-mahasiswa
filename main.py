from io import BytesIO
from typing import Union
from fastapi import FastAPI, HTTPException
import joblib
import requests

from src import CleaningText, KNNClassification, ExtractPdf
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

        predicted_label, probabilitas = knn.predict_label(CleaningText().remove_all(text))

        response = {
            'massage' : 'sukses memprediksi label',
            'data' : {
                'label-prediksi': knn.label_to_text(predicted_label),
                'probabilitas': knn.probabilitas_score_labels(probabilitas)
            }
        }

        return response
    
    except Exception as ex:

        response = {
            'massage' : 'error server',
            'error' : ex
        }

        return response
    
# test cleaning text
@app.post("/test-cleaning-text")
def test_cleaning_text(text: str)-> dict:

    if not text:
        raise HTTPException(status_code=400, detail="text perlu dimasukan")

    response = {
        'text-mentah' : text,
        'cleaning' : CleaningText().remove_all(text)
    }

    return response


@app.post("/test-reading-eksternal")
def test_reading_eksternal(path: str):
    if not path:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # validasi tipe file
    ValidateType(['.pdf']).validate_data(path)

    try:
        # Mendownload file PDF
        response = requests.get(path)
        response.raise_for_status()

        # Memeriksa apakah respons sukses
        if response.status_code == 200:
            # Membaca teks dari dokumen PDF
            extracted_text = ExtractPdf().extract_pdf_to_text(BytesIO(response.content))
            
            # Menampilkan teks yang diekstrak
            return extracted_text
        else:
            return "gagal dalam ekstrak teks"
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=404, detail="file not found")


# test reading file pdf
@app.get("/test-reading-classification")
def test_reading_file():
    file_pdf = "sample/pdf/docs-1.pdf"

    text = CleaningText().remove_all(ExtractPdf().extract_pdf_to_text(file_pdf))

    # loaded model
    knn_model = joblib.load('knn_classification_model/knn_classification_model.pkl')
    vectorizer = joblib.load('knn_classification_model/tfidf_fit_transform.pkl')

    knn = KNNClassification(knn_model, vectorizer)

    predicted_label, probabilitas = knn.predict_label(text)

    response = {
        'massage' : 'sukses memprediksi label',
        'data' : {
            'label-prediksi': knn.label_to_text(predicted_label),
            'probabilitas': knn.probabilitas_score_labels(probabilitas),
            'text-mentah' : text
        }
    }

    return response
