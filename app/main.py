from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
from app.routers import holidays

app = FastAPI(title="Public Holidays API")

# Include routers
app.include_router(holidays.router, prefix="/holidays", tags=["Holidays"])