import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src import ExtractPdf, Summerize


file_path = "sample/pdf/mpti2.pdf"

extracted_page = ExtractPdf().extract_pdf_to_text(file_path, start_page=0, end_page= 50, tipe="page")

find_page = ExtractPdf().find_target_text_page(extracted_page, target_kata=["abstrak", "pendahuluan"], hindari_kata=["daftar isi", "table of contents", "contents", "daftar pustaka", "bab ii"])

print(Summerize().summarize_text(find_page[0], 4), '\n\n\n', find_page[0])