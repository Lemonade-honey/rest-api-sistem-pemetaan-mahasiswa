from io import BytesIO
import os
import shutil
from typing import Union
import uuid
from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
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

@app.post("/test-reading-internal")
def test_reading_internal(path: str):
    if not path:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # validasi tipe file
    ValidateType(['.pdf']).validate_data(path)

    try:
        text = CleaningText().remove_all(ExtractPdf().extract_pdf_to_text(f"storages/{path}", 1, 2))

        return text
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=404, detail="file not found")

# test classification file pdf
@app.get("/test-reading-classification")
def test_reading_file():
    file_pdf = "sample/pdf/docs-1.pdf"

    text = CleaningText().remove_all(ExtractPdf().extract_pdf_to_text(file_pdf, 1, 2))

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

# test classification eksternal
@app.post("/classification-eksternal")
def classification_dokumen(file_path: str):
    # Validasi data
    if not file_path:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # validasi tipe file
    ValidateType(['.pdf']).validate_data(file_path)

    try:
        # Mendownload file PDF
        response = requests.get(file_path)
        response.raise_for_status()

        # Memeriksa apakah respons sukses
        if response.status_code == 200:
            # Membaca teks dari dokumen PDF
            extracted_text = ExtractPdf().extract_pdf_to_text(BytesIO(response.content), start_page=0, end_page=10)

            # cleaning text dokumen
            text = CleaningText().remove_all(extracted_text)
            
            # loaded model
            knn_model = joblib.load('knn_classification_model/knn_classification_model.pkl')
            vectorizer = joblib.load('knn_classification_model/tfidf_fit_transform.pkl')

            knn = KNNClassification(knn_model, vectorizer)

            predicted_label, probabilitas = knn.predict_label(text)

            response = {
                'status' : 'sukses',
                'massage' : 'sukses memprediksi label',
                'data' : {
                    'label-prediksi': knn.label_to_text(predicted_label),
                    'probabilitas': knn.probabilitas_score_labels(probabilitas),
                }
            }

            return response
        else:
            response = {
                'status' : 'gagal',
                'massage' : 'gagal dalam ekstrak file dokumen'
            }

            return response
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=404, detail="file not found")
    

# Upload File Dokumen
@app.post("/upload-file")
def upload_file(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File type is not PDF")
    
    try:
        # Generate unique filename
        new_filename = str(uuid.uuid4()) + ".pdf"
        
        # Define file location
        file_location = os.path.join("storages", new_filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return JSONResponse(content={"filename": new_filename}, status_code=200)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Delete File Folder
@app.delete("/delete-file")
def delete_file_path(file_path: str):
    if not file_path:
        raise HTTPException(status_code=403, detail="File Path tidak ada")
    
    try:
        if os.path.exists(f"storages/{file_path}"):
            # hapus path folder
            os.remove(f"storages/{file_path}")
            return JSONResponse(content={"massage" : "berhasil menghapus folder path"}, status_code=201)
        else:
            raise HTTPException(status_code=400, detail="Folder Path Tidak ditemukan")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))