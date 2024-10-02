import os
from typing import List, Optional, Any
from dotenv import load_dotenv
# from llama_index.llms import ChatMessage, MessageRole
from llama_index.core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from PIL import Image
import google.generativeai as genai
from llama_index.llms.gemini import Gemini
from llama_index.multi_modal_llms.gemini import GeminiMultiModal
from llama_index.core.program import MultiModalLLMCompletionProgram
from llama_index.core import SimpleDirectoryReader
import csv
import json
import time
from config import *
from setup_model import *
import nltk
nltk_data_dir = "/tmp/nltk_data"
nltk.download("punkt", download_dir=nltk_data_dir)

# Set the NLTK data path to the temporary directory
nltk.data.path.append(nltk_data_dir)


def save_pydantic_list_to_csv(pydantic_responses: List[InvoiceData], output_file: str):
    # Define the CSV headers
    headers = [
        "Invoice Number", "Date", "Shop Name", "Address",
        "SKU Name", "Quantity", "Rate", "Discount", "Tax", "Amount", "Total Amount"
    ]
    
    # Open the output file for writing
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header row
        writer.writerow(headers)
        
        # Iterate over each pydantic_response in the list
        for pydantic_response in pydantic_responses:
            # Access the invoice information
            invoice_info = pydantic_response.invoice_info
            
            # Iterate through each item in table_info
            for item in pydantic_response.table_info:
                # Prepare the row data
                row = [
                    invoice_info.invoice_number,
                    invoice_info.date,
                    invoice_info.shop_name,
                    invoice_info.address,
                    item.sku_name,
                    item.quantity,
                    item.rate,
                    item.discount,
                    item.tax,
                    item.amount,
                    item.total_amount
                ]
                
                # Write the row to the CSV file
                writer.writerow(row)

    print(f"All data successfully saved to {output_file}")


def save_pydantic_list_to_json(pydantic_responses: List[Any], output_file: str):
    # Create a list to hold all JSON data
    all_json_data = []
    
    # Iterate over each pydantic_response in the list
    for pydantic_response in pydantic_responses:
        # Access the invoice information
        invoice_info = pydantic_response.invoice_info
        
        # Iterate through each item in table_info
        for item in pydantic_response.table_info:
            # Create a dictionary combining invoice_info and the current item from table_info
            record = {
                "Invoice Number": invoice_info.invoice_number,
                "Date": invoice_info.date,
                "Shop Name": invoice_info.shop_name,
                "Address": invoice_info.address,
                "SKU Name": item.sku_name,
                "Quantity": item.quantity,
                "Rate": item.rate,
                "Discount": item.discount,
                "Tax": item.tax,
                "Amount": item.amount,
                "Total Amount": item.total_amount
            }
            # Add the record to the list
            all_json_data.append(record)
    
    # Write the JSON data to a file
    with open(output_file, 'w') as file:
        json.dump(all_json_data, file, indent=4)
    
    print(f"All data successfully saved to {output_file}")


def extract_invoice_data(image_path: str)->list[Any]:
    # Load the folder where the images are stored
    google_image_documents = SimpleDirectoryReader(image_path).load_data()
    # Initialise a list to store the invoice data
    invoices_data = []
    # Loop thorugh the images and get the data for the invoices
    for img_doc in google_image_documents:
        invoice_data = pydantic_gemini(
                output_class=InvoiceData,
                image_documents = [img_doc],
                prompt_template_str=prompt_template_str,
                model_name = "models/gemini-1.5-flash",
            )
        invoices_data.append(invoice_data)
    print(invoices_data)
    return invoices_data



# if __name__ == "__main__":
#     # Load the folder where the images are stored
#     image_path = r'C:\Users\faraz\Desktop\invoice_extraction\invoice_extraction\images'
#     google_image_documents = SimpleDirectoryReader(image_path).load_data()
#     # Initialise a list to store the invoice data
#     invoices_data = []
#     # Loop thorugh the images and get the data for the invoices
#     for img_doc in google_image_documents:
#         invoice_data = pydantic_gemini(
#                 output_class=InvoiceData,
#                 image_documents = [img_doc],
#                 prompt_template_str=prompt_template_str,
#                 model_name = "models/gemini-1.5-pro",
#             )
#         invoices_data.append(invoice_data)
#     print(invoices_data)
#     save_pydantic_list_to_csv(invoices_data, "combined_invoice_data.csv")
#     save_pydantic_list_to_json(invoices_data, "combined_invoice_data.json")




