import os
import shutil
from config import *


# function to empty the directory
def empty_directory(directory):
    # Delete all files inside the directory
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

# helper function to clean the directory
def initialise(folder):
    # initialise folders where data will be downloaded
    full_path = os.path.join(WORKING_DIRECTORY_PATH, folder)
    if not os.path.exists(full_path):
        os.makedirs(folder)
    else:
        empty_directory(folder)