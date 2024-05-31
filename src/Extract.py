from pdfminer.high_level import extract_text

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
            