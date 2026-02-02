from typing import List, Optional
from pydantic import BaseModel


class BiodataResponse(BaseModel):
    name: Optional[str]
    date_of_birth: Optional[str]
    time_of_birth: Optional[str]
    education: Optional[str]
    address: Optional[str]
    mobile_numbers: Optional[List[str]] = None
    email_addresses: Optional[List[str]] = None
