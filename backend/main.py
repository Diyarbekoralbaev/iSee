from fastapi import FastAPI, File, UploadFile, HTTPException
from func import generate_image_description, text_to_speech
from uuid import uuid4
import os
import shutil

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello from AralTech team!"}


@app.post("/generate_image_description/")
async def create_upload_file(file: UploadFile = File(...), lang: str = "en"):
    save_image_path = f"img/{uuid4()}.jpg"
    default_prompt = f"""
if detected traffic light follow this:    
Analyze the image and provide a concise description focusing on traffic lights only. Identify the color of each visible traffic light and estimate the approximate time remaining for pedestrians to cross based on standard timing protocols (if possible). Additionally, describe the number of visible roads and their approximate length, focusing only on elements within the road boundaries. Exclude irrelevant background information.

**Example Output:**

"There is one traffic light visible, currently showing red. Based on standard timing, approximately 30 seconds remain for pedestrians to cross. Two roads are visible, each approximately 20 meters long."

if detected medicine label follow this:

Analyze the image and extract the following information from the medicine label:

1. Brand name and generic name of the medicine
2. Dosage instructions, including quantity and frequency
3. Important warnings and precautions
4. Expiry date (if available)

Focus on accuracy and clarity, and present the information in a well-structured and easy-to-understand format. Avoid including irrelevant background information or marketing text.

**Example Output:**

"The medicine pictured is Acetaminophen 500mg tablets. Take one tablet every 4-6 hours, as needed. Do not exceed 4 grams (8 tablets) in 24 hours. Consult a doctor before use if pregnant, breastfeeding, or taking other medications. Expiry date: 2025-01-01."

Otherwise just decribe key elements of image.

"""
    with open(save_image_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        description = await generate_image_description(save_image_path, default_prompt, lang)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "iSee": description,
        "photo": f"{save_image_path}"
    }


@app.post("/chat_with_image/")
async def create_upload_file(prompt: str = "", lang: str = "en", photo: str = ""):
    prompt = f"{prompt}. Say in short terms"
    try:
        description = await generate_image_description(photo, prompt, lang)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "iSee": description,
        "photo": f"{photo}"
    }


@app.post("/text_to_speech/")
async def text_2_speech(text: str = ""):
    try:
        speech = await text_to_speech(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return speech


@app.delete("/delete_image/")
async def delete_image(photo: str = ""):
    try:
        os.remove(photo)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "message": "Image deleted"
    }