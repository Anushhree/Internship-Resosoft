from fastapi import APIRouter, UploadFile, File
from app.services import ocr_service
from app.models.biodata import BiodataResponse
from app.database import get_connection
import json

router = APIRouter(prefix="/ocr", tags=["OCR"])

@router.post("/extract", response_model=BiodataResponse)
async def extract_biodata(file: UploadFile = File(...)):
    """
    Upload a biodata document (JPG, PNG, PDF).
    Extracts Marathi + English text and returns JSON.
    """
    result = await ocr_service.process_document(file)
    return result
@router.get("/records")
def get_records():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM biodata")
    rows = cursor.fetchall()
    conn.close()
    # Convert rows to dicts and deserialize JSON fields
    records = []
    for r in rows:
        record = {
            "id": r[0],
            "name": r[1],
            "date_of_birth": r[2],
            "time_of_birth": r[3],
            "education": r[4],
            "address": r[5],
            "mobile_numbers": None,
            "email_addresses": None
        }
        # r[6] -> mobile_numbers, r[7] -> email_addresses
        try:
            if r[6]:
                record["mobile_numbers"] = json.loads(r[6])
        except Exception:
            record["mobile_numbers"] = None
        try:
            if r[7]:
                record["email_addresses"] = json.loads(r[7])
        except Exception:
            record["email_addresses"] = None
        records.append(record)

    return {"records": records}