from pdfminer.high_level import extract_text

class ExtractPdf:

    # extract pdf to text
    def extract_pdf_to_text(self, path_to_pdf: str)-> str:
        return extract_text(path_to_pdf)