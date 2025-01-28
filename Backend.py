from typing import Union, Dict
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import yt_dlp
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("Frontend.html", "r") as file:
        return file.read()

@app.post("/download")
def download_video(url: str = Form(...)) -> Dict[str, Union[str, int]]:
    ydl_opts = {
        'format': 'best',  # Download the best video quality
        'outtmpl': '%(title)s.%(ext)s'  # Save file with video title as filename
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return JSONResponse(content={"message": "Download complete!"})
