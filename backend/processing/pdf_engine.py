import pdfplumber
import re
from typing import List
from ..models import Voter
from .normalizer import normalize_bengali_text, convert_bengali_to_english_numerals

def parse_voter_cell(text: str) -> Voter:
    """
    Parses a single cell text to extract voter details.
    Expected format in cell involves Bengali labels.
    """
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Defaults
    voter = Voter()
    
    # Regex Patterns for specific fields
    # Note: These are heuristic patterns based on common layouts
    
    # Serial No often at the top or separate
    # Trying to find patterns like "নাম: ...", "পিতা: ..."
    
    # Normalize text first (remove zero-width spaces etc)
    text = normalize_bengali_text(text)
    
    # Name
    # Matches: নাম, নামঃ, নাম:, Nam
    name_match = re.search(r'(?:নাম|ভোটার|Name)\s*[:\-\s]\s*(.+)', text)
    if name_match:
        voter.name = name_match.group(1).strip()
    
    # Father / Husband
    # Matches: পিতা, স্বামী, Father, Husband
    father_match = re.search(r'(?:পিতা|স্বামী|Father|Husband)\s*[:\-\s]\s*(.+)', text)
    if father_match:
        voter.father_name = father_match.group(1).strip()
        
    # Mother
    # Matches: মাতা, Mother
    mother_match = re.search(r'(?:মাতা|Mother)\s*[:\-\s]\s*(.+)', text)
    if mother_match:
        voter.mother_name = mother_match.group(1).strip()
    
    # DOB (জন্ম তারিখ) - EXTRACT THIS FIRST before occupation
    # Matches: জন্ম তারিখ, Date of Birth. Improved to handle years like 19xx or 20xx
    # Handling potential newline after label
    dob_match = re.search(r'(?:জন্ম তারিখ|জন্ম|Date of Birth|DOB)\s*[:\-\s]*\s*([০-৯0-9\/.-]+)', text)
    if dob_match:
        voter.date_of_birth = convert_bengali_to_english_numerals(dob_match.group(1).strip())
        
    # Occupation (পেশা) - Extract AFTER DOB to avoid capturing DOB content
    # Stop at comma followed by জ (জন্ম) or at newline
    # Using negative lookahead or just stopping before comma
    occ_match = re.search(r'(?:পেশা|Occupation)\s*[:\-\s]\s*([^,\n]+)', text)
    if occ_match:
        voter.occupation = occ_match.group(1).strip()
        
    # ID (NID or Voter No) - strict digit capture
    # Prioritizes 17, 13, or 10 digit NIDs
    id_match = re.search(r'(?:ID|NID|NO|No)?\s*[:\-\s]*([০-৯0-9]{10,17})', text)
    if id_match:
        voter.voter_id = convert_bengali_to_english_numerals(id_match.group(1))
    
    # Address (ঠিকানা) - often the last few lines if not labeled
    addr_match = re.search(r'ঠিকানা\s*[:\-\s]\s*(.+)', text)
    if addr_match:
        voter.address = addr_match.group(1).strip()
    
    return voter

def parse_area_metadata(header_text: str) -> dict:
    """
    Parse area metadata from PDF header text.
    Expected to find: District, Upazila, Union, Ward, Voter Area, Area Code
    """
    metadata = {
        "district": None,
        "upazila": None,
        "union": None,
        "ward_number": None,
        "voter_area": None,
        "voter_area_code": None
    }
    
    if not header_text:
        return metadata
    
    # Normalize the header text
    header_text = normalize_bengali_text(header_text)
    
    # District (জেলা)
    # Stop before উপজেলা/থানা keywords
    district_match = re.search(r'(?:জেলা|District)\s*[:\-\s]*\s*(.+?)(?:\s+উপজেলা|\s+থানা|\n|$)', header_text, re.IGNORECASE)
    if district_match:
        metadata["district"] = district_match.group(1).strip()
    
    # Upazila (উপজেলা/থানা)
    # Match after উপজেলা or থানা keyword
    upazila_match = re.search(r'(?:উপজেলা|থানা)\s*[:\-\s/]*\s*([^\n,]+)', header_text, re.IGNORECASE)
    if upazila_match:
        metadata["upazila"] = upazila_match.group(1).strip()
    
    # Union (ইউনিয়ন/পৌরসভা)
    # Handle both ইউনিয়ন and পৌরসভা (municipality)
    union_match = re.search(r'(?:ইউনিয়ন|পৌরসভা|Union|Paurashava)\s*[:\-\s/]*\s*([^\n,]+?)(?:\s+ওয়ার্ড|\s+Ward|\n|$)', header_text, re.IGNORECASE)
    if union_match:
        metadata["union"] = union_match.group(1).strip()
    
    # Ward (ওয়ার্ড নং)
    # Handle multiple formats: "ওয়ার্ড নং", "Ward No", etc.
    ward_match = re.search(r'(?:ওয়ার্ড|Ward)\s*(?:নং|নম্বর|No\.?|Number)?\s*[:\-\s]*\s*([০-৯0-9]+)', header_text, re.IGNORECASE)
    if ward_match:
        metadata["ward_number"] = ward_match.group(1).strip()
    
    # Voter Area (ভোটার এলাকার নাম)
    # Match the area name and stop before "ভোটার এলাকার নম্বর" or area code
    area_match = re.search(r'(?:ভোটার এলাকার নাম|Voter Area Name|এলাকার নাম)\s*[:\-\s]*\s*(.+?)(?:\s*ভোটার এলাকার নম্বর|\s*নম্বর\s*:|\n|$)', header_text, re.IGNORECASE)
    if area_match:
        metadata["voter_area"] = area_match.group(1).strip()
    
    # Area Code (এলাকা কোড) - usually 4 digits
    code_match = re.search(r'(?:এলাকা কোড|Area Code|কোড)\s*[:\-\s]*\s*([০-৯0-9]{4})', header_text, re.IGNORECASE)
    if code_match:
        metadata["voter_area_code"] = code_match.group(1).strip()
    
    return metadata

def extract_voters_from_pdf(pdf_path: str, metadata: dict) -> List[Voter]:
    voters = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages):
            # Skip metadata extraction - use provided metadata directly
            
            # Grid Extraction
            tables = page.extract_tables({
                "vertical_strategy": "lines", 
                "horizontal_strategy": "lines",
                "intersection_y_tolerance": 5
            })
            
            # Flatten table rows
            for table in tables:
                for row in table:
                    # 'row' is a list of cells
                    if not row:
                        continue
                    
                    for cell in row:
                        if not cell:
                            continue
                        
                        # Clean the cell content
                        cell_text = cell.strip()
                        
                        # Basic validation: A voter cell usually has "নাম" or "Voter No"
                        if "নাম" not in cell_text and "name" not in cell_text.lower():
                            continue
                        
                        # Parse
                        voter_obj = parse_voter_cell(cell_text)
                        
                        # Fill Metadata from user input
                        voter_obj.district = metadata["district"]
                        voter_obj.upazila = metadata["upazila"]
                        voter_obj.union = metadata["union"]
                        voter_obj.ward_number = metadata["ward_number"]
                        voter_obj.voter_area = metadata["voter_area"]
                        voter_obj.voter_area_code = metadata["voter_area_code"]
                        
                        # Try to extract Serial No from cell text (often top left)
                        serial_match = re.search(r'^([০-৯0-9]+)', cell_text)
                        if serial_match:
                            voter_obj.serial_no = convert_bengali_to_english_numerals(serial_match.group(1))
                        
                        # Only add if we got at least a name
                        if voter_obj.name:
                            voters.append(voter_obj)
    
    # Post-processing: Fill in missing serial numbers
    voters = fill_missing_serial_numbers(voters)

    return voters

def fill_missing_serial_numbers(voters: List[Voter]) -> List[Voter]:
    """
    Fills in missing serial numbers by inferring from previous and next voters.
    """
    for i in range(len(voters)):
        if not voters[i].serial_no or voters[i].serial_no == "":
            # Try to infer from previous voter
            if i > 0 and voters[i-1].serial_no:
                try:
                    prev_serial = int(voters[i-1].serial_no)
                    voters[i].serial_no = str(prev_serial + 1).zfill(4)
                except (ValueError, AttributeError):
                    pass
            
            # If still missing, try to infer from next voter
            if (not voters[i].serial_no or voters[i].serial_no == "") and i < len(voters) - 1 and voters[i+1].serial_no:
                try:
                    next_serial = int(voters[i+1].serial_no)
                    voters[i].serial_no = str(next_serial - 1).zfill(4)
                except (ValueError, AttributeError):
                    pass
    
    return voters

def process_pdf(pdf_path: str, metadata: dict = None) -> List[Voter]:
    """
    Main entry point for processing a PDF.
    metadata: dict with keys: district, upazila, union, ward_number, voter_area, voter_area_code
    """
    if metadata is None:
        metadata = {
            "district": "Unavailable",
            "upazila": "Unavailable",
            "union": "Unavailable",
            "ward_number": "Unavailable",
            "voter_area": "Unavailable",
            "voter_area_code": "Unavailable"
        }
    
    return extract_voters_from_pdf(pdf_path, metadata)
