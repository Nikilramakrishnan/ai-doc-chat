from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    return {"status": "ok"}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)) -> dict:
    contents = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(contents),
    }
