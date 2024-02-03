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
import cv2
from PIL import Image 
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
shutil.rmtree('run/detect',ignore_errors=True)

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray

def model_pred(file_path,filename):
    try:
        detect="./runs/detect/predict/crops/licence"
        model = YOLO('best.pt')
    # Initialize EasyOCR reader
        reader = easyocr.Reader(['en'])
        # st.write(file_path)
        results = model.predict(file_path, save=True, save_crop=True, show_boxes=True)
        spliting=filename.split(".")
        for r in results:
            save_path=r.save_dir
        # st.write(r.save_dir)
    
    # Run OCR on the uploaded image using EasyOCR
        col1,col2=st.columns(2)
        with col1:
            # st.write(os.path.join(save_path, spliting[0]+".jpg"))
            image = Image.open(os.path.join(save_path, spliting[0]+".png"))

            st.image(image,use_column_width=True,caption='Predicted Image')
        save_path+="/crops/licence"
        with col2:
            image = Image.open(os.path.join(save_path, spliting[0]+".jpg"))

            st.image(image,use_column_width=True,caption='Croped image')
    
        
        print(spliting)
    
        crop_path=os.path.join(detect, spliting[0]+".jpg")
        save_path=os.path.join(save_path, spliting[0]+".jpg")
        # st.write(save_path)
        # st.write(crop_path)
        preprocessed=preprocess_image(save_path)
        result = reader.readtext(preprocessed)
        text = result[0][1]
        return text
    except Exception as e:
        print("eee")
        return e

# Streamlit UI
st.title("Please upload image")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg","png"])


if uploaded_file:
    try:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        image_bytes = uploaded_file.getvalue()
        file={"file": (uploaded_file.name, image_bytes, "image/jpeg")}
        
        with open(file_path, "wb") as image_file:
            image_file.write(uploaded_file.read())

        # st.write(uploaded_file)
        # Display the uploaded image
        st.image(uploaded_file)

        # Convert the image to bytes
        image_bytes = uploaded_file.getvalue()

        # Prepare the payload
        files = {"file": (uploaded_file.name, image_bytes, "image/jpeg")}
        result=model_pred(file_path,uploaded_file.name)
        st.subheader(f'Vehicle Number plate :  :blue[{result}]')
    except Exception as e:
        st.error(e)
    

    # Send the image to FastAPI
    # response = requests.post("http://localhost:8000/uploadfile", files=files)
    # st.toast(f"Image uploaded successfully")
    # if response.status_code == 200:
    #     result = response.json()
        
    #     st.subheader(f'{result["number_plate"]}')
    # else:
    #     st.error("Failed to upload image. Please try again.")
