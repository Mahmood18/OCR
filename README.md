# INVOICE_EXTRACTION

## Code files
### 1. api.py

A Flask-based API for extracting data from invoice images. This application allows users to upload multiple invoice images, processes them to extract relevant data, and provides the extracted information in both CSV and JSON formats. Additionally, users can download the compiled CSV file of the extracted data.

#### Features

- **Upload Multiple Images:** Accepts multiple invoice images in a single request limit upto 5 place on frontend.
- **Data Extraction:** Extracts relevant invoice data using OCR and other processing techniques.
- **Data Storage:** Saves extracted data in both CSV and JSON formats.
- **Download Extracted Data:** Allows users to download the compiled CSV file.

### 2. client.py

A script to manually test the `api.py` endpoints by sending HTTP requests.

#### Features

- **Send Images for Data Extraction:**
  - Upload multiple invoice images to the `/extract` endpoint.
  
- **Download Extracted Data:**
  - Retrieve the compiled CSV file from the `/download` endpoint.

#### Usage

1. **Configure Image Paths:**
   
   Update the `image_paths` list with the paths to your invoice images.

   ```python
   image_paths = [
       r"C:\path\to\image1.jpg",
       r"C:\path\to\image2.jpg",
       r"C:\path\to\image3.jpg",
       r"C:\path\to\image4.jpg"
   ]


### 3. config.py

Loads environment variables and configures application settings.

#### Features

- **Load Environment Variables:**
  - Utilizes `dotenv` to load variables from a `.env` file.
  
- **Configuration Variables:**
  - `MONGO_DB_URI`: MongoDB connection URI.
  - `GOOGLE_API_KEY`: Google API key.
  - `WORKING_DIRECTORY_PATH`: Path for working directories.
  - `HOST`: Host address for the server.
  - `PORT`: Port number for the server.
  - `BASE_URL`: Base URL of the API.

#### Usage

1. **Set Environment Variables:**

   Create a `.env` file in the root directory and define the necessary variables.

   ```env
   MONGO_DB_URI=your_mongodb_uri
   GOOGLE_API_KEY=your_google_api_key
   WORKING_DIRECTORY_PATH=/path/to/working/directory
   HOST=0.0.0.0
   PORT=5000
   BASE_URL=http://localhost:5000

### 4 database.py

Handles MongoDB setup and provides methods for database operations.

#### Features

- **MongoDB Connection:**
  - Establishes a connection to MongoDB using the URI from environment variables.
  
- **CRUD Operations:**
  - **Insert Single Document:** `insert_document(document)`
  - **Insert Multiple Documents:** `insert_documents(documents)`
  - **Find Single Document:** `find_document(query)`
  - **Find Multiple Documents:** `find_documents(query)`
  - **Update Document:** `update_document(query, update_fields)`
  - **Delete Single Document:** `delete_document(query)`
  - **Delete Multiple Documents:** `delete_documents(query)`

#### Usage

1. **Configure Environment Variables:**

   Ensure the `.env` file includes the `MONGO_DB_URI`.

   ```env
   MONGO_DB_URI=your_mongodb_uri


### 5. initialise_directories.py

Provides utility functions to manage and initialize directories for the application.

#### Features

- **Empty Directory:**
  - `empty_directory(directory)`: Removes all files and subdirectories within the specified directory.

- **Initialize Directory:**
  - `initialise(folder)`: Creates the directory if it doesn't exist; otherwise, it clears its contents.

#### Usage

1. **Import Functions:**

   ```python
   from initialise_directories import initialise




### 6 invoice_extraction.py

Handles the extraction of invoice data from images and saving the extracted information to CSV and JSON formats.

#### Features

- **Extract Invoice Data:**
  - Processes images to extract invoice details using a Pydantic-based model.
  
- **Save Extracted Data:**
  - Save extracted invoice data to a CSV file.
  - Save extracted invoice data to a JSON file.

#### Functions

- **`save_pydantic_list_to_csv(pydantic_responses: List[InvoiceData], output_file: str)`**
  
  - **Description:** Saves a list of `InvoiceData` Pydantic objects to a CSV file.
  - **Parameters:**
    - `pydantic_responses` (List[InvoiceData]): List of extracted invoice data.
    - `output_file` (str): Path to the output CSV file.
  - **Example:**
  
    ```python
    save_pydantic_list_to_csv(invoices_data, "combined_invoice_data.csv")
    ```

- **`save_pydantic_list_to_json(pydantic_responses: List[Any], output_file: str)`**
  
  - **Description:** Saves a list of `InvoiceData` Pydantic objects to a JSON file.
  - **Parameters:**
    - `pydantic_responses` (List[Any]): List of extracted invoice data.
    - `output_file` (str): Path to the output JSON file.
  - **Example:**
  
    ```python
    save_pydantic_list_to_json(invoices_data, "combined_invoice_data.json")
    ```

- **`extract_invoice_data(image_path: str) -> list[Any]`**
  
  - **Description:** Extracts invoice data from images located in the specified directory.
  - **Parameters:**
    - `image_path` (str): Path to the directory containing invoice images.
  - **Returns:** List of extracted `InvoiceData` objects.
  - **Example:**
  
    ```python
    invoices_data = extract_invoice_data('/path/to/images')
    ```

#### Usage

1. **Import Functions:**

   ```python
   from invoice_extraction import extract_invoice_data, save_pydantic_list_to_csv, save_pydantic_list_to_json



### 7 setup_model.py

Sets up and configures the Gemini multimodal language model for extracting invoice data from images.

#### Features

- **Pydantic Models:**
  - `TableInfo`: Represents individual table entries in an invoice.
  - `InvoiceInfo`: Represents header information of an invoice.
  - `InvoiceData`: Combines `InvoiceInfo` and a list of `TableInfo` for complete invoice data.
  
- **Gemini Model Initialization:**
  - Configures the Gemini multimodal LLM with the provided API key.
  
- **Prompt Template:**
  - Defines a structured prompt to guide the model in extracting necessary invoice information.
  
- **Data Extraction Function:**
  - `pydantic_gemini`: Processes image documents and extracts invoice data into Pydantic models.

#### Classes

- **`TableInfo`**
  
  - **Description:** Data model for individual table entries in an invoice.
  - **Fields:**
    - `sku_name`: SKU or Brand name.
    - `quantity`: Quantity of items.
    - `rate`: Rate per item.
    - `discount`: Applicable discount.
    - `tax`: Tax amount.
    - `amount`: Amount for the item.
    - `total_amount`: Total invoice amount.
  
- **`InvoiceInfo`**
  
  - **Description:** Data model for the header information of an invoice.
  - **Fields:**
    - `invoice_number`: Unique invoice number.
    - `date`: Date of the invoice.
    - `shop_name`: Name of the shop.
    - `address`: Address of the shop.
  
- **`InvoiceData`**
  
  - **Description:** Combines invoice header and table information.
  - **Fields:**
    - `invoice_info`: Instance of `InvoiceInfo`.
    - `table_info`: List of `TableInfo` instances.

#### Functions

- **`pydantic_gemini`**
  
  - **Description:** Extracts invoice data from image documents using the Gemini multimodal LLM and returns it as a Pydantic model.
  - **Parameters:**
    - `model_name` (str): Name of the Gemini model to use.
    - `output_class` (Type[BaseModel]): Pydantic model class for the output.
    - `image_documents` (List[Any]): List of image documents to process.
    - `prompt_template_str` (str): Prompt template guiding the extraction process.
  - **Returns:**
    - `BaseModel`: Instance of the specified Pydantic output class containing extracted data.
  - **Example:**
  
    ```python
    invoices_data = pydantic_gemini(
        model_name="models/gemini-1.5-flash",
        output_class=InvoiceData,
        image_documents=[img_doc],
        prompt_template_str=prompt_template_str,
    )
    ```

#### Usage

1. **Configure Environment Variables:**
   
   Ensure the `.env` file includes the `GOOGLE_API_KEY`.
   
   ```env
   GOOGLE_API_KEY=your_google_api_key
