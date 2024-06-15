from pdfminer.high_level import extract_text
import pdfplumber
import re

class ExtractPdf:

    # extract pdf to text
    def extract_pdf_to_text(self, path_to_pdf: str, tipe:str = "text", start_page:int = None, end_page:int = None)-> str | list:

        if tipe == 'text':
            if start_page is None and end_page is None:
                return extract_text(path_to_pdf)
            
            else:
                text_extract = ""
                for page_number in range(start_page, end_page + 1):
                    text_extract += extract_text(path_to_pdf, page_numbers=(page_number,))

                return text_extract
            
        elif tipe == 'page':
            page_extract = list()
            for page_number in range(start_page, end_page + 1):
                text = extract_text(path_to_pdf, page_numbers=(page_number,))
                text = re.sub(r'^[ \t\n\r\f\v]+$', '', text, flags=re.MULTILINE)
                text = re.sub(r'\n+', '\n', text).strip()

                if len(text) > 5 :
                    page_extract.append(text)

            return page_extract
        
        else:
            raise ValueError('tipe: {tipe} tidak valid')

    def find_target_text_page(self, extracted_page: list, target_kata:list, hindari_kata:list = None, page_number:bool = False)-> list | dict | None:

        page_target = dict() if page_number else list()

        for number, page in enumerate(extracted_page):

            page_lower = page.lower()

            if hindari_kata and any(keyword in page_lower for keyword in hindari_kata):
                continue # lanjut ke bawahnya dengan membawa data hindari

            if any(keyword in page_lower for keyword in target_kata):
                if page_number:
                    page_target[number] = page
                else:
                    page_target.append(page)

        return page_target

    # transkip nilai extract
    def extract_table_transkip(self, file_path: str)-> list:
        with pdfplumber.open(file_path) as pdf:
            table_halaman = []
            for table in pdf.pages:
                table_halaman.extend(table.extract_table())
        
        return table_halaman
    
    # membersihkan data table yang tidak dibutuhkan
    def cleaning_table(self, table: list)-> tuple:

        first_row = table[0:2]
        # menghapus 2 baris awal table
        del table[0:2]

        # hapus baris akhir
        last_row = table.pop()

        return table, last_row, first_row
    
    # memvalidasi bahwa transkip file beneran transkip file :)
    def validate_transkip(self, header_table: list)-> bool:

        valid_header = [
            [
                "No.",
                "Matakuliah",
                None,
                "SKS",
                "Nilai",
                "Bobot",
                "Nilai SKS"
            ],
            [
                None,
                "Kode",
                "Nama",
                None,
                None,
                None,
                None
            ]
        ]

        if header_table == valid_header:
            return True

        return False


    # mengelola data table menjadi bentuk yang sesuai untuk perhitungan score
    def get_nilai_transkip(self, table: list):

        transkip = {}
        
        try:
            # untuk tiap row table, ambil index 1 dan 4
            for data in table:
                transkip[data[1]] = data[4]

            # [kode, nilai huruf]
            return transkip
        
        except Exception as ex:

            return transkip