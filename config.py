from dotenv import load_dotenv
import os

load_dotenv()

# Fetch the api keys from the .env variable
MONGO_DB_URI = os.getenv('MONGO_DB_URI')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
WORKING_DIRECTORY_PATH = os.getenv('WORKING_DIRECTORY_PATH')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
BASE_URL = os.getenv('BASE_URL')

print(f"HOST: {HOST}")
print(f"PORT: {PORT}")
print(f"BASE_URL: {BASE_URL}")