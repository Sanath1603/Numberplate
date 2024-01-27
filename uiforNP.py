# import streamlit as st
# from PIL import Image
# st.header("Welcomme to Number PLate Detection ")
# st.write("kk")
# file=st.file_uploader("upload your file ",help="You can upload any type of image")
# # st.write(file.getvalue())
# if file is not None:
#     image=Image.open(file)
#     st.image(image)
# with st.sidebar:
#     st.write("Welcome")
import streamlit as st
import requests
import easyocr
from ultralytics import YOLO
import shutil
import os

def model_pred(file_path):
    shutil.rmtree('./run/detect/', ignore_errors=True)
    detect="./runs/detect/predict/crops/licence"
    model = YOLO('best.pt')
# Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])
    results = model.predict(file_path, save=True, save_crop=True, show_boxes=True)
    
    # Run OCR on the uploaded image using EasyOCR
    spliting=file_path.filename.split(".")
    print(spliting)
    crop_path=os.path.join(detect, spliting[0]+".jpg")
    result = reader.readtext(crop_path)
    text = result[0][1]
    return text

# Streamlit UI
st.title("Please upload image")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png"])

if uploaded_file:
    # Display the uploaded image
    st.image(uploaded_file)

    # Convert the image to bytes
    image_bytes = uploaded_file.getvalue()

    # Prepare the payload
    files = {"file": (uploaded_file.name, image_bytes, "image/jpeg")}
    result=model_pred(uploaded_file)
    st.subheader(f'{result}')

    # Send the image to FastAPI
    # response = requests.post("http://localhost:8000/uploadfile", files=files)
    # st.toast(f"Image uploaded successfully")
    # if response.status_code == 200:
    #     result = response.json()
        
    #     st.subheader(f'{result["number_plate"]}')
    # else:
    #     st.error("Failed to upload image. Please try again.")
