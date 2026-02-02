from app.utils import image_processing, ocr_engine
from app.models.biodata import BiodataResponse
from app.database import get_connection
import json

async def process_document(file):
    # Step 1: Preprocess image
    processed_image = image_processing.preprocess(file)

    # Step 2: OCR extraction
    text = ocr_engine.extract_text(processed_image)

    # Step 3: Parse fields
    parsed = {
        "name": ocr_engine.extract_name(text),
        "date_of_birth": ocr_engine.extract_dob(text),
        "time_of_birth": ocr_engine.extract_tob(text),
        "education": ocr_engine.extract_education(text),
        "address": ocr_engine.extract_address(text),
        "mobile_numbers": ocr_engine.extract_mobile(text) or None,
        "email_addresses": ocr_engine.extract_email(text) or None
    }

    # Add Marathi-formatted fields for response
    parsed["date_of_birth_marathi"] = ocr_engine.format_dob_marathi(parsed.get("date_of_birth"))
    parsed["time_of_birth_marathi"] = ocr_engine.format_tob_marathi(parsed.get("time_of_birth"))

    # Step 4: Store in SQLite (insert or update)
    conn = get_connection()
    cursor = conn.cursor()

    # Check if record exists by name
    cursor.execute("SELECT id FROM biodata WHERE name = ?", (parsed["name"],))
    existing = cursor.fetchone()

    # Serialize lists for storage in TEXT columns
    mobile_json = json.dumps(parsed["mobile_numbers"]) if parsed.get("mobile_numbers") else None
    email_json = json.dumps(parsed["email_addresses"]) if parsed.get("email_addresses") else None

    if existing:
        # Update existing record
        cursor.execute("""
            UPDATE biodata
            SET date_of_birth = ?, time_of_birth = ?, education = ?, address = ?, mobile_numbers = ?, email_addresses = ?
            WHERE id = ?
        """, (
            parsed["date_of_birth"],
            parsed["time_of_birth"],
            parsed["education"],
            parsed["address"],
            mobile_json,
            email_json,
            existing[0]
        ))
    else:
        # Insert new record
        cursor.execute("""
            INSERT INTO biodata (name, date_of_birth, time_of_birth, education, address, mobile_numbers, email_addresses)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            parsed["name"],
            parsed["date_of_birth"],
            parsed["time_of_birth"],
            parsed["education"],
            parsed["address"],
            mobile_json,
            email_json
        ))

    conn.commit()
    conn.close()

    # Return response object
    return BiodataResponse(**parsed)