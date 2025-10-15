from PyPDF2 import PdfReader
from io import BytesIO

def load_pdf(content: bytes) -> str:
    reader = PdfReader(BytesIO(content))
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def load_text(content: bytes) -> str:
    return content.decode("utf-8")
