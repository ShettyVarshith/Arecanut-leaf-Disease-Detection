import streamlit as st
import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras import models
import time
import base64


# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #BAD2D5;
        font-family: 'Arial', sans-serif;
    }
    .navbar-container {
        width: 100%;
        display: flex;
        justify-content: space-between;  /* Changed from flex-end to space-between */
        align-items: center;  /* Center the items vertically */
        background-color: #343a40;
        padding: 20px 0;  /* Increased padding for greater height */
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        margin-top: 40px;
    }
    .navbar-left {
        display: flex;
        align-items: center;
        padding-left: 20px;  /* Adjust padding for alignment */
    }
    .navbar-left img {
        border-radius: 50%;
        width: 70px;
        height: 70px;  /* Adjust height for consistency */
    }
    .navbar-left span {
        font-size: 1.5rem;  /* Font size for the text next to the logo */
        font-weight: bold;
        margin-left: 10px;  /* Margin between the logo and the text */
        color: #fff;  /* White text color */
    }
    .navbar {
        display: flex;
        justify-content: flex-end;
        padding: 0 100px;  /* Adjusted padding */
    }
    .navbar a {
        color: white;
        text-decoration: none;
        padding: 10px 10px;  /* Increased padding for larger clickable area */
        border-radius: 4px;
        font-size: 1.05rem;  /* Increased font size for better readability */
        background-color: transparent;  /* Set background color to transparent */
        margin-left: 1px;  /* Adjusted margin between buttons */
    }
    .navbar a:hover {
        color: #28a745 !important; /* Green text color on hover */
        text-decoration: underline; 
    }
    .title {
        font-family: 'Times New Roman', Times, serif;
        color: #333333;
        text-align: center;
        margin-top: 80px; /* Adjust for fixed navbar with increased height */
    }
    </style>
""", unsafe_allow_html=True)

# Encode the image in base64
file_ = open("static/areca seed.jfif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

# Navigation bar with direct links
st.markdown(f"""
    <div class="navbar-container">
        <div class="navbar-left">
            <img src="data:image/png;base64,{data_url}" alt="Arecanut Disease Detection Logo">
            <span>ArecaNut Leaf Detection</span>
        </div>
        <div class="navbar">
            <a href="http://127.0.0.1:5000/" target="_blank">Home</a>
            <a href="http://127.0.0.1:5000/help" target="_blank">Help</a>
            <a href="http://127.0.0.1:5000/contact" target="_blank">Contact</a>
            <a href="http://127.0.0.1:5000/feedback" target="_blank">Feedback</a>
        </div>
    </div>
""", unsafe_allow_html=True)


# Title with custom class for styling
st.markdown('<h1 class="title">Arecanut Leaf Spot Disease Detection</h1>', unsafe_allow_html=True)

def predict(image):
    classifier_model = 'InceptionModel.h5'
    model = models.load_model(classifier_model)
    from tensorflow.keras import applications
    inceptionv3 = applications.InceptionV3(include_top=False, weights='imagenet')
    test_image = cv2.resize(image, (150, 150))
    test_image = np.array(test_image)
    test_image = test_image / 255.0
    test_image = np.expand_dims(test_image, axis=0)
    preds = model.predict(test_image)
    class_names = {0: 'Diseased', 1: 'Non-Diseased'}
    result = f"Predicted as {class_names[np.argmax(preds)]} with {(max(preds[0])*100).__round__(2)} % confidence. "
    return result

file_uploaded = st.file_uploader("Choose File", type=["png", "jpg", "jpeg"])
class_btn = st.button("CHECK")
if file_uploaded is not None:
    image = cv2.imdecode(np.frombuffer(file_uploaded.getvalue(), np.uint8), cv2.IMREAD_UNCHANGED)
    st.image(image, caption='Uploaded Image', use_column_width=True)

if class_btn:
    if file_uploaded is None:
        st.write("Invalid command, please upload an image")
    else:
        with st.spinner('Model working....'):
            predictions = predict(image)
            time.sleep(1)
            st.success('Prediction Successful.')
            st.write(predictions)
