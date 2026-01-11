from pydantic import BaseModel
from typing import Optional

class Voter(BaseModel):
    serial_no: Optional[str] = None
    name: Optional[str] = None
    voter_id: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    occupation: Optional[str] = None
    date_of_birth: Optional[str] = None
    address: Optional[str] = None
    
    # Area Metadata (repeated for each voter as per request)
    district: Optional[str] = None
    upazila: Optional[str] = None
    union: Optional[str] = None
    ward_number: Optional[str] = None
    voter_area: Optional[str] = None
    voter_area_code: Optional[str] = None

class ExtractionResult(BaseModel):
    job_id: str
    status: str
    total_voters: int
    data: list[Voter]
