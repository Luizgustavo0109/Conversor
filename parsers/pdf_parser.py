from PyPDF2 import PdfReader

class PdfParser:
    def parse(self, file_path: str) -> dict:
        reader = PdfReader(file_path)
        paragraphs = [page.extract_text() for page in reader.pages]
        return {"type": "pdf", "content": paragraphs}