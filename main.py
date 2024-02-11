from fastapi import FastAPI, File, UploadFile, HTTPException
from func import generate_image_description
from uuid import uuid4
import os
import shutil

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from AralTech team!"}


@app.post("/generate_image_description/")
async def create_upload_file(file: UploadFile = File(...), prompt: str = "describe this image in 15 words"):
    save_image_path = f"img/{uuid4()}.jpg"
    with open(save_image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        description = generate_image_description(save_image_path, prompt)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        os.remove(save_image_path)
    return {"description": description}
