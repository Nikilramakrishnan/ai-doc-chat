#print("🔥 RUNNING FILE:", __file__)
from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import pandas as pd
import ollama
from io import BytesIO

app = FastAPI()

document_text = ""



@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    global document_text
    document_text = ""

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        reader = PdfReader(file.file)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                document_text += text + "\n"

    elif filename.endswith(".xlsx"):
        contents = file.file.read()      # ✅ read bytes
        excel_data = BytesIO(contents)   # ✅ make it seekable
        df = pd.read_excel(excel_data)   # ✅ pandas-friendly
        document_text = df.to_string()

    else:
        return {"error": "Unsupported file type"}

    return {"message": "File uploaded successfully"}



@app.post("/chat")
def chat(question: str):
    global document_text

    if not document_text:
        return {"error": "No document uploaded"}

    doc_snippet = document_text[:3000]  # LIMIT SIZE

    prompt = f"""
Answer the question using ONLY the document below.

DOCUMENT:
{doc_snippet}

QUESTION:
{question}
"""

    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return {"answer": response["message"]["content"]}
