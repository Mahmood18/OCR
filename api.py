# import os
# import shutil
# from flask import Flask, request, jsonify, send_file
# from PIL import Image
# from typing import List
# from initialise_directories import *
# from invoice_extraction import *
# from config import *

# app = Flask(__name__)



# IMAGE_DIR = os.path.join(WORKING_DIRECTORY_PATH, 'images')
# OUTPUT_DIR = os.path.join(WORKING_DIRECTORY_PATH, 'output')

# @app.route('/extract', methods=['POST'])
# def extract_data():
#     print("Recieved Hit extract")
#     initialise(IMAGE_DIR)
#     initialise(OUTPUT_DIR)

#     data = request.files
#     images = data.getlist("images")
    
#     if not images:
#         return jsonify({'error': 'No images provided'}), 400
    
#     # Save each image to the directory
#     for i, image in enumerate(images):
#         image_path = os.path.join(IMAGE_DIR, f"image_{i}.jpg")
#         image.save(image_path)
    
#     # Extract the images data
#     invoices_data = extract_invoice_data(IMAGE_DIR)
    
#    # Save the data to CSV and JSON
#     csv_path = os.path.join(OUTPUT_DIR, 'combined_invoice_data.csv')
#     json_path = os.path.join(OUTPUT_DIR, 'combined_invoice_data.json')
#     save_pydantic_list_to_csv(invoices_data, csv_path)
#     save_pydantic_list_to_json(invoices_data, json_path)
    
#     # Read the JSON data from the file
#     with open(json_path, 'r') as file:
#         all_json_data = json.load(file)
    
#     # Return the JSON data as a response
#     return jsonify({
#         'message': 'Data extraction successful',
#         'number_of_images_processed': len(images),
#         'data': all_json_data
#     }), 200


# @app.route('/download', methods=['GET'])
# def download_file():
#     print("Recieved Hit Download")
#     csv_path = os.path.join(OUTPUT_DIR, 'combined_invoice_data.csv')
    
#     if not os.path.exists(csv_path):
#         return jsonify({'error': 'CSV file not found'}), 404
    
#     return send_file(csv_path, as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True, host=HOST, port=PORT)






import streamlit as st
import requests
import pandas as pd
import os
from PIL import Image
import json
from initialise_directories import *
from invoice_extraction import *
from config import *

# Determine the base API URL (remove this part since Flask is not used anymore)
# BASE_URL code and print statements are removed.

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #000000;
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 2px 2px 12px rgba(255, 255, 255, 0.1);
    }
    .stButton button {
        background-color: #0073e6;
        color: #ffffff;  /* Button text color */
        padding: 10px 20px;
        border-radius: 5px;
        border: none;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #005bb5;
    }
    .stFileUploader label {
        font-weight: bold;
        color: #000000;  /* File uploader label color */
    }
    .stSelectbox div, .stTextInput div, .stNumberInput div, .stTextArea div {
        color: #000000;  /* Dropdown and input text color */
    }
    .stSelectbox, .stTextInput, .stNumberInput, .stTextArea {
        background-color: #333333;  /* Input background color */
    }
    .stDownloadButton button {
        color: #000000;  /* Download button text color */
    }
    .stTitle, .css-1d391kg {
        color: #ffffff !important;  /* Title color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize directories
IMAGE_DIR = os.path.join(WORKING_DIRECTORY_PATH, 'images')
OUTPUT_DIR = os.path.join(WORKING_DIRECTORY_PATH, 'output')

initialise(IMAGE_DIR)
initialise(OUTPUT_DIR)

# Set the title of the app
st.markdown("<h1 style='color: #ffffff;'>Invoice Extractor</h1>", unsafe_allow_html=True)

# Dropdown menu to select single or multiple images
option = st.selectbox(
    "Select Mode:",
    ("Single Image", "Multiple Images")
)

# File uploader based on the dropdown selection
allowed_formats = ["png", "jpg", "jpeg"]

def validate_file_format(uploaded_file):
    if uploaded_file:
        file_format = uploaded_file.name.split('.')[-1].lower()
        if file_format not in allowed_formats:
            st.error(f"File format not correct. Supported formats are: {', '.join(allowed_formats).upper()}")
            return False
        return True
    return False

uploaded_file = None
uploaded_files = None

if option == "Single Image":
    uploaded_file = st.file_uploader("Upload an Image", type=allowed_formats)
    if uploaded_file and not validate_file_format(uploaded_file):
        uploaded_file = None
else:
    uploaded_files = st.file_uploader("Upload Images", type=allowed_formats, accept_multiple_files=True)
    if uploaded_files:
        if len(uploaded_files) > 5:
            st.error("You can only upload up to 5 images at a time.")
            uploaded_files = None
        else:
            valid_files = [f for f in uploaded_files if validate_file_format(f)]
            if len(valid_files) < len(uploaded_files):
                uploaded_files = valid_files

# Extract button - Disabled until images are uploaded
extract_button = st.button("Extract", disabled=(not uploaded_file if option == "Single Image" else not uploaded_files))

# Initialize variables
extracted_data = None
download_button_disabled = True

# Function to extract invoice data locally without API
def extract_data_local(files):
    if isinstance(files, list):
        for i, file in enumerate(files):
            image = Image.open(file)
            image_path = os.path.join(IMAGE_DIR, f"image_{i}.jpg")
            image.save(image_path)
    else:
        image = Image.open(files)
        image_path = os.path.join(IMAGE_DIR, "image_0.jpg")
        image.save(image_path)

    # Extract invoice data
    invoices_data = extract_invoice_data(IMAGE_DIR)

    # Save the data to CSV and JSON
    csv_path = os.path.join(OUTPUT_DIR, 'combined_invoice_data.csv')
    json_path = os.path.join(OUTPUT_DIR, 'combined_invoice_data.json')
    save_pydantic_list_to_csv(invoices_data, csv_path)
    save_pydantic_list_to_json(invoices_data, json_path)

    # Read and return JSON data
    with open(json_path, 'r') as file:
        all_json_data = json.load(file)
    return all_json_data

# Handle extraction and display results
if extract_button:
    if option == "Single Image":
        extracted_data = extract_data_local([uploaded_file])
    else:
        extracted_data = extract_data_local(uploaded_files)

    if extracted_data is not None:
        st.json(extracted_data)  # Display the JSON data
        download_button_disabled = False  # Enable the download button

# Enable the download button after extraction
if not download_button_disabled:
    with open(os.path.join(OUTPUT_DIR, 'combined_invoice_data.csv'), 'rb') as file:
        st.download_button("Download CSV", file, file_name='combined_invoice_data.csv')

    with open(os.path.join(OUTPUT_DIR, 'combined_invoice_data.json'), 'rb') as file:
        st.download_button("Download JSON", file, file_name='combined_invoice_data.json')
