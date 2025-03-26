from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse

from cryptography.fernet import Fernet
import os

from encryption import encrypt_data, generate_key, decrypt_data

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Change this to [""] for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not os.path.exists("secret.key"):
    with open("secret.key", "wb") as key_file:
        key_file.write(Fernet.generate_key())

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def load_key():
    return open("secret.key", "rb").read()

key = load_key()
cipher = Fernet(key)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    file_content = await file.read()
    encrypted_content = encrypt_data(file_content)

    with open(file_path, "wb") as f:
        f.write(encrypted_content)

    return {"message": "File uploaded and encrypted successfully", "filename": file.filename}

@app.get("/download/{filename}")
async def download_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}

    with open(file_path, "rb") as f:
        encrypted_content = f.read()
    
    decrypted_content = decrypt_data(encrypted_content)

    decrypted_path = file_path + ".decrypted"
    with open(decrypted_path, "wb") as f:
        f.write(decrypted_content)

    return {"filename": filename, "content": decrypted_content.decode(errors="ignore")}

@app.delete("/delete/{filename}")
async def delete_file(filename: str):
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": f"File '{filename}' deleted successfully"}
    
    raise HTTPException(status_code=404, detail="File not found")
