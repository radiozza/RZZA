from fastapi import FastAPI, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import shutil
import os
from database import get_db, init_db, Song
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
@app.on_event("startup")
def startup_event(): init_db()
@app.get("/playlist")
def read_playlist(db: Session = Depends(get_db)):
    songs = db.query(Song).all()
    return [{"id": s.id, "title": s.title, "artist": s.artist} for s in songs]
@app.post("/upload")
async def upload_music(title: str, artist: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    music_dir = "/app/music" 
    if not os.path.exists(music_dir): os.makedirs(music_dir)
    file_location = f"{music_dir}/{file.filename}"
    with open(file_location, "wb+") as buffer: shutil.copyfileobj(file.file, buffer)
    db_song = Song(title=title, artist=artist, filename=file.filename)
    db.add(db_song); db.commit(); db.refresh(db_song)
    return {"status": "success", "filename": file.filename}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
