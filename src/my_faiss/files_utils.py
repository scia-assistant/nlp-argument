import hashlib

import pdfplumber


def get_pdf_text_hash(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "".join(page.extract_text() for page in pdf.pages if page.extract_text())
    text_hash = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return text, text_hash


def chunk_text(text, chunk_size):
    words = text.split()
    chunks = [
        " ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)
    ]
    return chunks
