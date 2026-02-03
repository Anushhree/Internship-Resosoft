from fastapi import APIRouter, HTTPException
from app.models.holiday_request import HolidayRequest
from app.services.holidays_service import fetch_holidays

router = APIRouter()

@router.post("/")
def get_public_holidays(request: HolidayRequest):
    try:
        holidays = fetch_holidays(request.country_code, request.year)
        return {"country_code": request.country_code, "year": request.year, "holidays": holidays}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))