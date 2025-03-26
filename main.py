from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import os

from encryption import encrypt_data, decrypt_data  # Ensure encryption.py exists

app = FastAPI()

# 🔹 CORS Configuration (Restrict in Production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Change to actual frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔹 Directories
UPLOAD_FOLDER = "uploads"
UPLOAD_ORIGINAL = os.path.join(UPLOAD_FOLDER, "original")
UPLOAD_ENC = os.path.join(UPLOAD_FOLDER, "encrypted")
os.makedirs(UPLOAD_ORIGINAL, exist_ok=True)
os.makedirs(UPLOAD_ENC, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "VanishVault API is running 🚀"}

# 🔹 File Upload
@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save original file
    original_path = os.path.join(UPLOAD_ORIGINAL, file.filename)
    file_content = await file.read()
    with open(original_path, "wb") as f:
        f.write(file_content)

    # Encrypt and save encrypted file
    encrypted_content = encrypt_data(file_content)
    encrypted_path = os.path.join(UPLOAD_ENC, file.filename + ".enc")
    with open(encrypted_path, "wb") as f:
        f.write(encrypted_content)

    return {"message": "File uploaded & encrypted successfully", "filename": file.filename}

# 🔹 Secure File Download
@app.get("/download/{filename}")
async def download_file(filename: str):
    encrypted_path = os.path.join(UPLOAD_ENC, filename + ".enc")  # Ensure correct path

    if not os.path.exists(encrypted_path):
        raise HTTPException(status_code=404, detail="File not found")

    with open(encrypted_path, "rb") as f:
        encrypted_content = f.read()

    decrypted_content = decrypt_data(encrypted_content)

    return StreamingResponse(
        iter([decrypted_content]),
        media_type="application/octet-stream",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )

# 🔹 List Files
@app.get("/filelist/")
async def file_list():
    files = os.listdir(UPLOAD_ORIGINAL)
    return {"files": files}

# 🔹 Delete File (Both Encrypted & Original)
@app.delete("/delete/{filename}")
async def delete_file(filename: str):
    original_path = os.path.join(UPLOAD_ORIGINAL, filename)
    encrypted_path = os.path.join(UPLOAD_ENC, filename + ".enc")

    if os.path.exists(original_path):
        os.remove(original_path)
    
    if os.path.exists(encrypted_path):
        os.remove(encrypted_path)

    if not os.path.exists(original_path) and not os.path.exists(encrypted_path):
        return {"message": f"File '{filename}' deleted successfully"}
    
    raise HTTPException(status_code=404, detail="File not found")
