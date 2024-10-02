import requests
import base64

# Example image paths
image_paths = [
    r"C:\Users\faraz\Desktop\images\1697435386852.jpg",
    r"C:\Users\faraz\Desktop\images\1697442284440.jpg",
    r"C:\Users\faraz\Desktop\images\1697443161694.jpg",
    r"C:\Users\faraz\Desktop\images\1697443467077.jpg"
]

# API endpoint
url_extract = "http://127.0.0.1:5000/extract"
url_download = "http://127.0.0.1:5000/download"

# # Prepare the files to send
# files = [('images', open(image_path, 'rb')) for image_path in image_paths]

# # Send the POST request to the API
# response_extract = requests.post(url_extract, files=files)
# # Print the response from the API
# print(response_extract.status_code)
# print(response_extract.json())

# # Close the file handles
# for _, file in files:
#     file.close()

response_download = requests.get(url_download)
print(response_download)