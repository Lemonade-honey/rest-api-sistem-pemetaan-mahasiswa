from pdfminer.high_level import extract_text
import pdfplumber

class ExtractPdf:

    # extract pdf to text
    def extract_pdf_to_text(self, path_to_pdf: str, start_page:int = None, end_page:int = None)-> str:
        if start_page is None and end_page is None:
            return extract_text(path_to_pdf)
        
        else:
            text_extract = ""
            for page_number in range(start_page, end_page + 1):
                text_extract += extract_text(path_to_pdf, page_numbers=(page_number,))

            return text_extract
            
    # transkip nilai extract
    def extract_table_transkip(self, file_path: str)-> list:
        with pdfplumber.open(file_path) as pdf:
            table_halaman = []
            for table in pdf.pages:
                table_halaman.extend(table.extract_table())
        
        return table_halaman
    
    # membersihkan data table yang tidak dibutuhkan
    def cleaning_table(self, table: list)-> tuple:
        # menghapus 2 baris awal table
        del table[0:2]

        # hapus baris akhir
        last_table = table.pop()

        return table, last_table
    
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