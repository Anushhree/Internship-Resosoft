from pydantic import BaseModel

class HolidayRequest(BaseModel):
    country_code: str
    year: int