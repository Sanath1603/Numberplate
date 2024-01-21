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

    # Send the image to FastAPI
    response = requests.post("http://localhost:8000/uploadfile", files=files)
    st.toast(f"Image uploaded successfully")
    if response.status_code == 200:
        result = response.json()
        
        st.subheader(f'{result["number_plate"]}')
    else:
        st.error("Failed to upload image. Please try again.")
