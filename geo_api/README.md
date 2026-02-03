# 🌍 Geocode FastAPI Project

This project provides a FastAPI service to fetch geographical coordinates (latitude and longitude) for a given place name.  
Coordinates are retrieved using OpenStreetMap’s Nominatim API and stored in a SQLite database.

---

## 📂 Project Structure
project-root/ │ ├── app/ │   ├── init.py │   ├── main.py              # FastAPI entry point │   ├── database.py          # SQLite connection + table creation │   ├── models.py            # Pydantic schemas │   └── routers/ │       ├── init.py │       └── geocode.py       # Place → coordinates endpoint │ ├── images.db                # SQLite database file (stores places table) ├── requirements.txt         # Dependencies └── README.md

---

## ⚙️ Setup Instructions

### 1. Clone and enter project
```bash
git clone <your-repo-url>
cd project-root



2. Create virtual environment
python -m venv venv
# Activate
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


3. Install dependencies
pip install -r requirements.txt


4. Initialize database
Tables (places) are auto‑created on server startup.
5. Run server
uvicorn app.main:app --reload

🚀 API Endpoints
Geocode
- POST /geocode/
- Request:
{ "place": "Eiffel Tower" }
- Response:
{
  "place": "Eiffel Tower",
  "latitude": 48.8582602,
  "longitude": 2.2944991
}


Coordinates are also stored in images.db under the places table.



✅ Notes
- Uses OpenStreetMap’s free Nominatim API (no API key required).
- SQLite (images.db) stores place name + latitude + longitude.
- Swagger UI available at: http://127.0.0.1:8000/docs

📌 Requirements
- Python 3.9+
- Dependencies: fastapi, uvicorn, pydantic, requests

---

This README is **ready to paste** into your project root.  
Would you like me to also add a **GET `/places/{id}` endpoint** section in the README so you can retrieve stored coordinates later, just like you did for images?

