from pydantic import BaseModel

class LocationRequest(BaseModel):
    place_name: str

class CoordinatesResponse(BaseModel):
    latitude: float
    longitude: float