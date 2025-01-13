from docx import Document

class DocxParser:
    def parse(self, file_path: str) -> dict:
        document = Document(file_path)
        paragraphs = [p.text for p in document.paragraphs if p.text.strip()]    
        return {"type": "docx", "content": paragraphs}