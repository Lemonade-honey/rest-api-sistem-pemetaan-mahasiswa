import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import ExtractPdf


file_path = "sample/pdf/docs-1.pdf"

extracted_page = ExtractPdf().extract_pdf_to_text(file_path, start_page=0, end_page= 10, tipe="page")

find_page = ExtractPdf().find_target_text_page(extracted_page, target_kata=["ringkasan"])

print(find_page)