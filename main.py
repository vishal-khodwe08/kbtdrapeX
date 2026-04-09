from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os

from drape import generate_saree_tryon

app = FastAPI()

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html") as f:
        return f.read()


@app.post("/tryon/")
async def tryon(person: UploadFile = File(...), saree: UploadFile = File(...)):

    person_path = f"{UPLOAD_FOLDER}/{person.filename}"
    saree_path = f"{UPLOAD_FOLDER}/{saree.filename}"

    with open(person_path, "wb") as buffer:
        shutil.copyfileobj(person.file, buffer)

    with open(saree_path, "wb") as buffer:
        shutil.copyfileobj(saree.file, buffer)

    result_path = generate_saree_tryon(person_path, saree_path)

    return {"result": result_path}


app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")