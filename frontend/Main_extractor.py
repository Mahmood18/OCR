import streamlit as st
import requests
import pandas as pd

import sys
import os
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

# Determine the base API URL
if BASE_URL:
    # Remove any trailing slash to prevent double slashes in endpoints
    print("1")
    base_api_url = BASE_URL.rstrip('/')
else:
    print("1")
    base_api_url = f"http://{HOST}:{PORT}"

print(base_api_url)

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

def main():
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

    # Function to send image(s) to the API and get the response as JSON
    def extract_data(files):
        files_data = [('images', (file.name, file, file.type)) for file in files] if isinstance(files, list) else [('images', (files.name, files, files.type))]
        
        # Display loader while waiting for the response
        with st.spinner('Extracting data...'):
            response = requests.post(f"{base_api_url}/extract", files=files_data)
            if response.status_code == 200:
                return response.json()
            else:
                st.error("Failed to extract data")
                return None

    # Handle extraction and display results
    if extract_button:
        if option == "Single Image":
            extracted_data = extract_data([uploaded_file])
        else:
            extracted_data = extract_data(uploaded_files)
        
        if extracted_data is not None:
            st.json(extracted_data)  # Display the JSON data
            download_button_disabled = False  # Enable the download button

    # Enable the download button after extraction
    download_button = st.button("Download as CSV", disabled=download_button_disabled)

    # If download button is pressed, call the backend API to get the CSV
    if download_button:
        st.write("Press the download button")  # Debugging log

        try:
            csv_response = requests.get(f"{base_api_url}/download")
            st.write("Request sent, awaiting response...")  # Debugging log

            if csv_response.status_code == 200:
                # Immediately trigger CSV download
                st.download_button(
                    label="Click here to download",
                    data=csv_response.content,
                    file_name='extracted_data.csv',
                    mime='text/csv',
                )
            else:
                st.write(f"Failed to download CSV, status code: {csv_response.status_code}")  # Debugging log
                st.error("Failed to download CSV")
        except Exception as e:
            st.write(f"Exception occurred: {e}")  # Debugging log
            st.error("An error occurred while trying to download the CSV.")

if __name__ == "__main__":
    main()