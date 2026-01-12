from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import shutil
import os
import sys
import uuid
import webbrowser
from .processing.pdf_engine import process_pdf
from .models import ExtractionResult

# Function to get resource path for PyInstaller
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

app = FastAPI(title="Bengali Voter Parser")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.join(os.path.abspath("."), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/api/upload", response_model=ExtractionResult)
async def upload_file(
    file: UploadFile = File(...),
    district: str = Form(""),
    upazila: str = Form(""),
    union: str = Form(""),
    ward_number: str = Form(""),
    voter_area: str = Form(""),
    voter_area_code: str = Form("")
):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Create metadata dict from form inputs
        metadata = {
            "district": district or "Unavailable",
            "upazila": upazila or "Unavailable",
            "union": union or "Unavailable",
            "ward_number": ward_number or "Unavailable",
            "voter_area": voter_area or "Unavailable",
            "voter_area_code": voter_area_code or "Unavailable"
        }
        
        # Convert Bengali numerals to English in metadata
        from .processing.normalizer import convert_bengali_to_english_numerals
        if metadata["ward_number"] != "Unavailable":
            metadata["ward_number"] = convert_bengali_to_english_numerals(metadata["ward_number"])
        if metadata["voter_area_code"] != "Unavailable":
            metadata["voter_area_code"] = convert_bengali_to_english_numerals(metadata["voter_area_code"])
            
        # Processing with user-provided metadata
        voters = process_pdf(file_path, metadata)
        
        return ExtractionResult(
            job_id=file_id,
            status="completed",
            total_voters=len(voters),
            data=voters
        )
            
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files (Frontend) - Must be after API routes
# We check if static directory exists (it will be present in distributed exe)
static_path = resource_path("static")
if os.path.exists(static_path):
    app.mount("/", StaticFiles(directory=static_path, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # Open browser on startup (only for manual script run)
    webbrowser.open("http://localhost:8000")
    
    from multiprocessing import freeze_support
    freeze_support()
    uvicorn.run(app, host="0.0.0.0", port=8000)
