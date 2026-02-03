from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import pandas as pd
import os

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def root():
    return {"message": "AI Doc Chat backend running"}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    text = ""

    if file.filename.endswith(".pdf"):
        reader = PdfReader(file_path)
        for page in reader.pages:
            text += page.extract_text()

    elif file.filename.endswith(".xlsx"):
        df = pd.read_excel(file_path)
        text = df.to_string()

    else:
        return {"error": "Unsupported file type"}

    return {
        "filename": file.filename,
        "text_preview": text[:500]
    }
