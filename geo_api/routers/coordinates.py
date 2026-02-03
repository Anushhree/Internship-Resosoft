from fastapi import APIRouter, HTTPException
from geopy.geocoders import Nominatim
from models import LocationRequest, CoordinatesResponse
from database import get_coordinates_from_db, save_coordinates_to_db

router = APIRouter()
geolocator = Nominatim(user_agent="geo_api")

@router.post("/get-coordinates", response_model=CoordinatesResponse)
def get_coordinates(request: LocationRequest):
    # Step 1: Check DB cache
    cached = get_coordinates_from_db(request.place_name)
    if cached:
        return CoordinatesResponse(latitude=cached[0], longitude=cached[1])

    # Step 2: Fetch from geocoder
    location = geolocator.geocode(request.place_name)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    # Step 3: Save to DB
    save_coordinates_to_db(request.place_name, location.latitude, location.longitude)

    return CoordinatesResponse(latitude=location.latitude, longitude=location.longitude)