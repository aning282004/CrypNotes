from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from typing import List, Optional
from uuid import uuid4
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Simulasi DB notes, setiap note dict berisi id, title, content, username, file_url
notes_db = []

@router.post("/create")
async def create_note(
    title: str = Form(...),
    content: str = Form(...),
    username: str = Form(...),
    file: Optional[UploadFile] = File(None)
):
    file_url = None
    if file:
        filename = f"{uuid4()}_{file.filename}"
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        file_url = f"/files/{filename}"

    note = {
        "id": str(uuid4()),  # ID unik untuk tiap note
        "title": title,
        "content": content,
        "username": username,
        "file_url": file_url
    }
    notes_db.append(note)
    return {"message": "Note saved", "note": note}

@router.get("/", response_model=List[dict])
def get_notes():
    return notes_db

@router.delete("/delete/{note_id}")
def delete_note(note_id: str):
    global notes_db
    note = next((n for n in notes_db if n["id"] == note_id), None)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    # Hapus file jika ada
    if note.get("file_url"):
        file_path = note["file_url"].replace("/files/", UPLOAD_DIR + "/")
        if os.path.exists(file_path):
            os.remove(file_path)

    notes_db = [n for n in notes_db if n["id"] != note_id]
    return {"message": "Note deleted successfully"}
