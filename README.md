# Marathi OCR API

An OCR-powered FastAPI service for extracting structured biodata fields from Marathi documents (e.g., matrimonial biodata).  
The service preprocesses uploaded images, runs OCR, and parses key fields such as **Name, Date of Birth, Time of Birth, Education, Address, Mobile Numbers, and Email Addresses**.  
Extracted data is stored in a SQLite database and returned as JSON.

---

## 🚀 Features
- Image preprocessing for better OCR accuracy
- OCR text extraction using Tesseract
- Field parsers for:
  - Name (`नाव`)
  - Date of Birth (`जन्म तारीख`)
  - Time of Birth (`जन्म वेळ`)
  - Education (`शिक्षण`)
  - Address (`पत्ता`)
  - Mobile Numbers (`मो. नं.` / `मोबाईल नंबर`)
  - Email Addresses
- SQLite storage with insert/update logic
- FastAPI endpoints returning structured JSON

---

## 📂 Project Structure
marath_ocr_api/
├── app/ │ 
   ├── models/ 
        -biodata.py         # Pydantic & SQLAlchemy models │  
   ├── routers/  
        -ocr_routes.py       # FastAPI routes │ 
   ├── services/ 
        -ocr_service.py       # Business logic (ocr_service.py) │ 
   ├── utils/   
        -image_processing.py
        -ocr_engine.py        # OCR engine & image preprocessing │
   ├── database.py      # SQLite connection helper │  
   ├── main.py          # FastAPI entrypoint │
   ├── config.py
├── scripts.py
├── tests/               # Unit tests 
├── requirements.txt     # Python dependencies 
├── README.md            # Project documentation


---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/Anushhree/Internship-Resosoft.git
cd marath_ocr_api

### 2. Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows

### 3. Install requirements 
pip install -r requirements.txt

### 4. Run database migrations
Make sure your biodata table has the following columns:
- id, name, date_of_birth, time_of_birth, education, address, mobile_numbers, email_addresses
if misssing add with :
ALTER TABLE biodata ADD COLUMN mobile_numbers TEXT;
ALTER TABLE biodata ADD COLUMN email_addresses TEXT;

### 5. Start the API
uvicorn app.main:app --reload

-----------------

📡 Usage
Endpoint
POST /ocr
Example Request
Upload a biodata image:
curl -X POST "http://127.0.0.1:8000/ocr" \
  -F "file=@sample_biodata.jpg"

EXAMPLE RESPONSE:
{
  "name": "आर्य विजयताय देशमुख",
  "date_of_birth": "07-04-1997",
  "time_of_birth": "मंगळवार 07:13",
  "education": "B.E. (Software Engineering)",
  "address": "नागपूर",
  "mobile_numbers": "9437844877, 8341344989",
  "email_addresses": "aaryad@gmail.com"
}


-------------


📌 Notes
- OCR accuracy depends on image quality. Preprocessing (grayscale, thresholding) improves results.
- Mobile numbers are extracted only if prefixed with मो. नं. or मोबाईल नंबर.
- Email addresses are matched using standard regex.




