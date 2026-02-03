Public Holidays API (FastAPI + SQLite)
📌 Overview
This project is a FastAPI application that fetches public holidays for a given country and year using the Nager.Date Public Holidays API.
Fetched holidays are both returned to the client and stored in a local SQLite database for persistence and caching.

⚙️ Features
- POST /holidays/ → Accepts country_code and year, fetches holidays from Nager.Date API.
- SQLite Integration → Stores holidays in public_holidays table (app/database.db).
- Modular Structure → Routers, services, and models are separated for clean architecture.
- Validation → Pydantic models ensure correct input types.


📂 Project Structure
project/
│── app/
│   │── main.py              # Entry point
│   │── config.py            # Configs (API base URL)
│   │── routers/
│   │   │── holidays.py      # API routes
│   │── services/
│   │   │── holidays_service.py  # External API + DB logic
│   │── models/
│   │   │── holiday_request.py   # Request model
│   │── db.py                # Initializes SQLite table
│── requirements.txt

🛠️ Setup
1. Install dependencies
pip install -r requirements.txt

2. Initialize the database
Run:
python app/db.py


This creates app/database.db with a public_holidays table.

3. Start the FastAPI server
uvicorn app.main:app --reload


Server runs at:
👉 http://127.0.0.1:8000
Swagger docs available at:
👉 http://127.0.0.1:8000/docs

📤 Example Usage
Request
POST /holidays/
Content-Type: application/json

{
  "country_code": "IN",
  "year": 2025
}


Response
{
  "country_code": "IN",
  "year": 2025,
  "holidays": [
    {
      "date": "2025-01-26",
      "localName": "गणतंत्र दिवस",
      "name": "Republic Day",
      "countryCode": "IN",
      "fixed": true,
      "global": true,
      "counties": null,
      "launchYear": null,
      "type": "Public"
    },
    ...
  ]
}



🗄 Database Schema
CREATE TABLE IF NOT EXISTS public_holidays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country_code TEXT NOT NULL,
    year INTEGER NOT NULL,
    date TEXT NOT NULL,
    local_name TEXT,
    name TEXT,
    fixed BOOLEAN,
    global BOOLEAN,
    counties TEXT,
    launch_year INTEGER,
    type TEXT
);



🔄 Workflow
- Client sends request → /holidays/.
- FastAPI validates input.
- Service calls Nager.Date API.
- Holidays are saved into SQLite (public_holidays).
- Response returned to client.

📚 External API
- Name: Nager.Date Public Holidays API
- Base URL: https://date.nager.at/api/v3/PublicHolidays/{year}/{countryCode}

