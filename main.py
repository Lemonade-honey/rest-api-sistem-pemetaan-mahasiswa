from io import BytesIO
import os
import random
import shutil
import uuid
from fastapi import FastAPI, HTTPException, File, Request, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse, Response
import joblib
import requests

from src import CleaningText, KNNClassification, ExtractPdf, TranskipScores, AchievementTranskip
from static import StaticMatakuliah
from model import File
from request import ValidateType

app = FastAPI()
origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
                'data' : {
                    'label-prediksi': knn.label_to_text(predicted_label),
                    'probabilitas': knn.probabilitas_score_labels(probabilitas),
                }
            }

            return response
        else:
            raise HTTPException(status_code=504, detail="file tidak dapat dibaca")
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=404, detail="file not found")


# classification internal
@app.post("/classification-internal")
def classification_internal(folder_file_path: str):
    if not folder_file_path:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # validasi tipe file
    ValidateType(['.pdf']).validate_data(folder_file_path)

    if not os.path.exists(f"storages/document/{folder_file_path}"):
        raise HTTPException(status_code=404, detail="File target tidak valid atau tidak ditemukan")
    
    try:
        # Membaca teks dari dokumen PDF
        extracted_text = ExtractPdf().extract_pdf_to_text(f"storages/document/{folder_file_path}", start_page=0, end_page=10)

        # cleaning text dokumen
        text = CleaningText().remove_all(extracted_text)
        
        # loaded model
        knn_model = joblib.load('knn_classification_model/knn_classification_model.pkl')
        vectorizer = joblib.load('knn_classification_model/tfidf_fit_transform.pkl')

        knn = KNNClassification(knn_model, vectorizer)

        predicted_label, probabilitas = knn.predict_label(text)

        response = {
            'data' : {
                'label-prediksi': knn.label_to_text(predicted_label),
                'probabilitas': knn.probabilitas_score_labels(probabilitas),
            }
        }

        return response
    
    except requests.exceptions.HTTPError:
        raise HTTPException(status_code=404, detail="file not found")
    


# Upload File Dokumen
@app.post("/upload-file-document")
async def upload_file(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File type is not PDF")
    
    try:
        # Generate random folder name
        folder_name = str(random.randint(1000000, 9999999))
        folder_path = os.path.join("storages/document", folder_name)
        
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Define file location
        file_location = os.path.join(folder_path, file.filename)
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return f"{folder_name}/{file.filename}"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Delete File Folder
@app.delete("/revert-file-document")
async def delete_file_path(request: Request):
    if not request:
        raise HTTPException(status_code=403, detail="id File Path tidak ada")
    
    try:
        body_request = await request.json()

        # mengambil 7 digit awal text
        body_request = body_request[:7]
        print(body_request)

        # Periksa apakah folder tersebut ada
        if os.path.exists(f"storages/document/{body_request}"):
            # Menghapus folder beserta semua isinya
            shutil.rmtree(f"storages/document/{body_request}")

            return True
        else:
            raise HTTPException(status_code=400, detail="Folder Path Tidak ditemukan")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# menampilkan isi file
@app.get('/library')
async def show_document(folder_path: str, type: str = None):
    if not folder_path:
        raise HTTPException(status_code=403, detail="File Path tidak ada")
    
    if type == 'document' or not type:
        if os.path.exists(f"storages/document/{folder_path}"):
            return FileResponse(f"storages/document/{folder_path}", media_type='application/pdf')
    if type == 'transkip' :
        if os.path.exists(f"storages/transkip/{folder_path}"):
            return FileResponse(f"storages/transkip/{folder_path}", media_type='application/pdf')
        
    raise HTTPException(status_code=404, detail="Folder Path Tidak ditemukan")
        
# upload file transkip
@app.post('/upload-file-transkip')
async def upload_file_transkip(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="File type is not PDF")
    
    try:
        os.makedirs("storages/transkip", exist_ok=True)

        # Generate random folder name
        folder_name = str(random.randint(1000000, 9999999))
        folder_path = os.path.join("storages/transkip", folder_name)
        
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)
        
        # Define file location with the new filename
        file_extension = os.path.splitext(file.filename)[1]  # get the file extension
        file_name = str(uuid.uuid4()) + file_extension
        file_location = os.path.join(folder_path, file_name)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return f"{folder_name}/{file_name}"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# revert file filepound
@app.delete('/revert-file-transkip')
async def delete_file_transkip(request: Request):
    if not request:
        raise HTTPException(status_code=403, detail="id File Path tidak ada")
    
    try:
        body_request = await request.json()

        # mengambil 7 digit awal text
        body_request = body_request[:7]
        print(body_request)

        # Periksa apakah folder tersebut ada
        if os.path.exists(f"storages/transkip/{body_request}"):
            # Menghapus folder beserta semua isinya
            shutil.rmtree(f"storages/transkip/{body_request}")

            return True
        else:
            raise HTTPException(status_code=400, detail="Folder Path Tidak ditemukan")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.post('/transkip-nilai-scores')
def transkip_nilai_scores(folder_file_path: str):
    if not folder_file_path:
        raise HTTPException(status_code=400, detail="No files provided")
    
    # validasi tipe file
    ValidateType(['.pdf']).validate_data(folder_file_path)

    if not os.path.exists(f"storages/transkip/{folder_file_path}"):
        raise HTTPException(status_code=404, detail="File target tidak valid atau tidak ditemukan")
    
    try:

        extract_table = ExtractPdf().extract_table_transkip(f"storages/transkip/{folder_file_path}")

        extract_table, last_row, first_row = ExtractPdf().cleaning_table(extract_table)

        # validate struktur
        if not ExtractPdf().validate_transkip(first_row):
            raise HTTPException(status_code=406, detail="Struktur file tidak sesuai")

        # label scores
        nilai_transkip = ExtractPdf().get_nilai_transkip(extract_table)
        transkip_scores = TranskipScores().fill_empty_labels(TranskipScores().label_transkip_nilai(nilai_transkip))

        # akademik scores
        akademik_scores = TranskipScores().point_of_transkip_nilai(last_row)

        # badge
        badge = AchievementTranskip().badge_achievement_transkip(nilai_transkip)

        return {
            'transkip-label-score' : transkip_scores,
            'akademik-scores' : akademik_scores,
            'badge' : badge
        }
    
    except Exception as ex:
        print(ex)
        raise HTTPException(status_code=506, detail="server error")

@app.delete("/delete-file-document")
async def delete_file_document(folder: str):
    if not folder:
        raise HTTPException(status_code=403, detail="id File Path tidak ada")
    
    try:
       # Periksa apakah folder tersebut ada
        if os.path.exists(f"storages/document/{folder}"):
            # Menghapus folder beserta semua isinya
            shutil.rmtree(f"storages/document/{folder}")

            return True
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))