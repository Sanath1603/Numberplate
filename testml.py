from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.requests import Request
import easyocr
from ultralytics import YOLO
import shutil
import os
app = FastAPI()

# Enable CORS (Cross-Origin Resource Sharing)
origins = ["*"]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=[""], allow_headers=[""])

# Add TrustedHostMiddleware to prevent host header attacks
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Load the YOLO model
model = YOLO('best (1).pt')

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
shutil.rmtree('C:/Users/sanat/Downloads/runs/detect', ignore_errors=True)
detect="C:/Users/sanat/Downloads/runs/detect/predict/crops/licence"
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    # Save the uploaded file
    # filename = file.filename
    # with open(filename, "wb") as f:
    #     f.write(file.file.read())
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as image_file:
        image_file.write(file.file.read())


    # Run inference on the uploaded image using YOLO
    results = model.predict(file_path, save=True, save_crop=True, show_boxes=True)
    
    # Run OCR on the uploaded image using EasyOCR
    spliting=file.filename.split(".")
    print(spliting)
    crop_path=os.path.join(detect, spliting[0]+".jpg")
    result = reader.readtext(crop_path)
    text = result[0][1]

    return JSONResponse(content={"number_plate": text,})