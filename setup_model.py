import os
from typing import List, Optional, Any, Type
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
from config import *

# Define Pydantic models
class TableInfo(BaseModel):
    """Data model for Table Info"""
    sku_name: Optional[str] = None
    quantity: Optional[str] = None
    rate: Optional[str] = None
    discount: Optional[str] = None
    tax: Optional[str] = None
    amount: Optional[str] = None
    total_amount: Optional[str] = None

class InvoiceInfo(BaseModel):
    """Data model for Header info for invoices"""
    invoice_number: Optional[str] = None
    date: Optional[str] = None
    shop_name: Optional[str] = None
    address: Optional[str] = None

class InvoiceData(BaseModel):
    """Data model for invoices"""
    invoice_info: InvoiceInfo
    table_info: List[TableInfo]

# Initialize Gemini
genai.configure(api_key=GOOGLE_API_KEY)
# Create Pydantic output parser
output_parser = PydanticOutputParser(InvoiceData)

# Define the prompt template to guide the model
prompt_template_str = """
The attached image is an invoice. Please extract the following information:

1. Invoice Information:
   - Invoice Number
   - Date of the Invoice
   - Shop Name
   - Address

2. Table Information (for each item):
   - SKU Name
   - Quantity
   - Rate
   - Discount
   - Tax
   - Amount
   - Total Amount of Invoice

Note: 
- Understand the structure of the invoice before determining any values. Invoice Information occurs at the top and then the table information occurs next.
- Header names may vary for Invoice Information and Table Information fields Eg: SKU Name can be Brand and vice versa. Abbreviations of headers might be used Eg: Quantity can be Qty. Use your judgment to map required fields from invoice to the requested fields.
- Return empty for any unclear or missing information.
- Avoid using commas within values (e.g., use 4435.00 instead of 4,435.00).
- Data can be in both english and Urdu. Translate the Urdu text into relevent English text for the required field.

Provide the output in the specified format.
"""


def pydantic_gemini(
    model_name: str, 
    output_class: Type[BaseModel], 
    image_documents: List[Any],  # You can replace Any with the specific type you expect for image documents
    prompt_template_str: str
) -> BaseModel:
    gemini_llm = GeminiMultiModal(
        api_key=GOOGLE_API_KEY, model_name=model_name
    )

    llm_program = MultiModalLLMCompletionProgram.from_defaults(
        output_parser=PydanticOutputParser(output_class),
        image_documents=image_documents,
        prompt_template_str=prompt_template_str,
        multi_modal_llm=gemini_llm,
        verbose=True,
    )

    response = llm_program()
    return response





