
import pytesseract
import re
from app.config import OCR_LANGUAGES
import json

# Point to the installed Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text(image):
    # Use Marathi + English for mixed documents
    return pytesseract.image_to_string(image, lang=OCR_LANGUAGES)
# --- Field extraction helpers ---

def extract_name(text: str):
    name_labels = ["नाव", "नाम", "Name", "Full Name"]
    for line in text.splitlines():
        for lbl in name_labels:
            if lbl in line:
                parts = re.split(r'[:\-–—।]\s*', line, maxsplit=1)
                if len(parts) > 1 and parts[1].strip():
                    return parts[1].strip()
                # if label present but no separator, remove label and return rest
                candidate = line.replace(lbl, "").strip()
                if candidate:
                    return candidate

    # Fallback: use first non-empty line that doesn't look like a labeled field
    skip_tokens = ['जन्म', 'DOB', 'मो', 'मोबाइल', 'पत्ता', 'फोन', 'Phone', 'Email', 'ई-मेल']
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if any(tok in line for tok in skip_tokens):
            continue
        # require at least a few letters (Devanagari or Latin)
        if len(re.sub(r"[^A-Za-z\u0900-\u097F]", "", line)) > 2:
            return line

    return None

import re

MARATHI_MONTHS = {
    "जानेवारी": "01", "फेब्रुवारी": "02", "मार्च": "03", "एप्रिल": "04",
    "मे": "05", "जून": "06", "जुलै": "07", "ऑगस्ट": "08",
    "सप्टेंबर": "09", "ऑक्टोबर": "10", "नोव्हेंबर": "11", "डिसेंबर": "12"
}

# Reverse mapping: number -> Marathi month name
NUM_TO_MARATHI = {v: k for k, v in MARATHI_MONTHS.items()}

def format_dob_marathi(dob: str):
    """Convert a DOB like '12-01-1990' or '12 January 1990' to Marathi month name format.
    Returns e.g. '12 जानेवारी 1990' or None if input empty/invalid.
    """
    if not dob:
        return None
    # Try numeric date first
    m = re.search(r"(\d{1,2})\D+(\d{1,2})\D+(\d{2,4})", dob)
    if m:
        day, mon, year = m.group(1), m.group(2).zfill(2), m.group(3)
        mar = NUM_TO_MARATHI.get(mon)
        if mar:
            return f"{int(day):02d} {mar} {year}"
        else:
            return f"{int(day):02d}-{mon}-{year}"

    # Try textual month (Marathi or English)
    m2 = re.search(r"(\d{1,2})\s+([\w\u0900-\u097F]+)\s+(\d{4})", dob)
    if m2:
        day, mon_token, year = m2.group(1), m2.group(2).strip(), m2.group(3)
        if mon_token in MARATHI_MONTHS:
            mon = MARATHI_MONTHS[mon_token]
            mar = NUM_TO_MARATHI.get(mon)
            return f"{int(day):02d} {mar} {year}"
        # english month fallback (simple mapping)
        en_map = {
            'january':'जानेवारी','february':'फेब्रुवारी','march':'मार्च','april':'एप्रिल','may':'मे',
            'june':'जून','july':'जुलै','august':'ऑगस्ट','september':'सप्टेंबर','october':'ऑक्टोबर',
            'november':'नोव्हेंबर','december':'डिसेंबर'
        }
        mar = en_map.get(mon_token.lower())
        if mar:
            return f"{int(day):02d} {mar} {year}"

    return None

def format_tob_marathi(tob: str):
    """Convert time strings into a readable Marathi time, e.g. '05:30 AM' -> '05:30 पूर्व'"""
    if not tob:
        return None
    # Look for HH:MM and optional AM/PM
    m = re.search(r"(\d{1,2})\s*[:.]\s*(\d{2})(?:\s*(AM|PM|am|pm))?", tob)
    if m:
        hour, minute, period = int(m.group(1)), int(m.group(2)), (m.group(3) or '').upper()
        mar_period = None
        if period == 'AM':
            mar_period = 'पूर्व'
        elif period == 'PM':
            mar_period = 'दुपारी'
        if mar_period:
            return f"{hour:02d}:{minute:02d} {mar_period}"
        return f"{hour:02d}:{minute:02d}"

    # Fallback: single hour with AM/PM
    m2 = re.search(r"(\d{1,2})\s*(AM|PM|am|pm)", tob)
    if m2:
        hour = int(m2.group(1))
        period = m2.group(2).upper()
        mar_period = 'पूर्व' if period == 'AM' else 'दुपारी'
        return f"{hour:02d}:00 {mar_period}"

    return None

def extract_dob(text: str):
    lines = text.splitlines()
    for line in lines:
        if "जन्म तारीख" in line or "जन्मतारीख" in line:
            tokens = line.split()
            # Look for pattern: number + month + year
            for i in range(len(tokens)-2):
                if tokens[i].isdigit() and tokens[i+2].isdigit():
                    day = tokens[i]
                    mar_month = tokens[i+1]
                    year = tokens[i+2]
                    month = MARATHI_MONTHS.get(mar_month.strip(), mar_month)
                    return f"{day.zfill(2)}-{month}-{year}"
    return None

def extract_tob(text: str):
    # Search labeled lines first, then fallback to all lines
    candidates = []
    for line in text.splitlines():
        if re.search(r'जन्म.*वेळ|जन्मवेळ|Time\s*of\s*Birth|Birth\s*Time|जन्म\s*वेळ', line, re.I):
            candidates.append(line)
    if not candidates:
        candidates = text.splitlines()

    for line in candidates:
        # Match HH:MM or H:MM with optional AM/PM
        m = re.search(r'(\d{1,2})\s*[:.]\s*(\d{2})(?:\s*(AM|PM|am|pm))?', line)
        if m:
            hour, minute, period = m.group(1), m.group(2), (m.group(3) or '').upper()
            return f"{hour.zfill(2)}:{minute.zfill(2)} {period}".strip()

        # Match H MM or Hh MM with optional AM/PM
        m2 = re.search(r'(\d{1,2})\s+[hH]?\s*(\d{1,2})(?:\s*(AM|PM|am|pm))?', line)
        if m2:
            hour, minute, period = m2.group(1), m2.group(2), (m2.group(3) or '').upper()
            return f"{hour.zfill(2)}:{minute.zfill(2)} {period}".strip()

        # Single hour with AM/PM
        m3 = re.search(r'\b(\d{1,2})\s*(AM|PM|am|pm)\b', line)
        if m3:
            hour, period = m3.group(1), m3.group(2).upper()
            return f"{hour.zfill(2)}:00 {period}"

    return None

def get_month(mar_month):
    for key in MARATHI_MONTHS.keys():
        if mar_month.startswith(key[:3]):  # match first 3 letters
            return MARATHI_MONTHS[key]
    return mar_month

def debug_birth_lines(text: str):
    for line in text.splitlines():
        if "जन्म" in line:
            print("DEBUG:", line)

def get_month(mar_month):
    for key in MARATHI_MONTHS.keys():
        if mar_month.startswith(key[:3]):
            return MARATHI_MONTHS[key]
    return mar_month   
        
import re
def normalize_text(text: str):
    text = re.sub(r"[^\w\sअ-ह]", " ", text)  # remove punctuation
    text = re.sub(r"\s+", " ", text)         # collapse spaces
    return text.strip()


def devanagari_to_ascii(s: str) -> str:
    if not s:
        return s
    trans = str.maketrans({
        '०':'0','१':'1','२':'2','३':'3','४':'4','५':'5','६':'6','७':'7','८':'8','९':'9'
    })
    return s.translate(trans)

def extract_education(text: str):
    edu_labels = ["शिक्षण", "शिक्षा", "Qualification", "पढाई"]
    degree_pattern = re.compile(r"\b(B\.?A\.?|M\.?A\.?|BSc|MSc|BCom|BCOM|BE|B\.E|M\.E|PhD|बी\.?ए|एम\.?ए|बीएससी)\b", re.I)
    for line in text.splitlines():
        for lbl in edu_labels:
            if lbl in line:
                parts = re.split(r'[:\-–—।]\s*', line, maxsplit=1)
                if len(parts) > 1 and parts[1].strip():
                    return parts[1].strip()
                candidate = line.replace(lbl, "").strip()
                if candidate:
                    return candidate

    # Try to find degree-like tokens anywhere
    for line in text.splitlines():
        if degree_pattern.search(line):
            return line.strip()

    return None

def extract_mobile(text: str):
    # Normalize Devanagari digits to ASCII so regexes match
    norm_text = devanagari_to_ascii(text)

    # First, try to find lines explicitly labeled as mobile/phone in Marathi or English
    mobile_labels = ['मो. नं', 'मो. नं.', 'मो.नं', 'मो.नं.', 'मो.', 'मोबाईल', 'मोबाईल नंबर', 'मोबाइल नंबर', 'मोबाइल', 'संपर्क','संपर्क क्रमांक','Phone', 'फोन']
    numbers = []
    lines = norm_text.splitlines()
    for idx, line in enumerate(lines):
        for lbl in mobile_labels:
            if lbl in line:
                # look at this line and the following up to 2 lines (labels sometimes on previous line)
                to_check = [line]
                if idx + 1 < len(lines):
                    to_check.append(lines[idx+1])
                if idx + 2 < len(lines):
                    to_check.append(lines[idx+2])

                for chk in to_check:
                    for cand in re.findall(r'[\d\-\s\+]{6,20}', chk):
                        digits = re.sub(r'\D', '', cand)
                        if len(digits) >= 10:
                            n = digits[-10:]
                            numbers.append(n)

                if numbers:
                    return list(dict.fromkeys(numbers))

    # Fallback: robustly find mobile numbers anywhere in text (after normalization)
    candidates = re.findall(r'[\d\-\s\+]{10,30}', norm_text)
    for cand in candidates:
        digits = re.sub(r'\D', '', cand)
        if len(digits) >= 10:
            n = digits[-10:]
            numbers.append(n)

    # Also catch any contiguous 10+ digit sequences that may have been missed
    for d in re.findall(r'\d{10,}', norm_text):
        n = d[-10:]
        numbers.append(n)

    numbers = list(dict.fromkeys(numbers))
    return numbers if numbers else None

def extract_email(text: str):
    matches = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    # normalize to lowercase and deduplicate
    emails = [m.lower() for m in matches]
    emails = list(dict.fromkeys(emails))
    return emails if emails else None

def extract_address(text: str):
    addr_labels = ['पत्ता', 'Address', 'ठिकाण', 'ठिकाण:', 'पत्ता:']
    lines = text.splitlines()
    for idx, line in enumerate(lines):
        for lbl in addr_labels:
            if lbl in line:
                # take remainder of line after label
                parts = re.split(r'[:\-–—]\s*', line, maxsplit=1)
                remainder = parts[1].strip() if len(parts) > 1 else line.replace(lbl, '').strip()
                # also append following non-empty lines (up to 3) to capture multi-line addresses
                extra = []
                for j in range(idx+1, min(idx+4, len(lines))):
                    ln = lines[j].strip()
                    if not ln:
                        break
                    # stop if next line looks like another labeled field
                    if re.search(r'\b(जन्म|नाव|मो|फोन|Email|ई-मेल|शिक्षण)\b', ln):
                        break
                    extra.append(ln)
                addr = ' '.join([remainder] + extra).strip()
                return addr if addr else None

    # Fallback: try to find a line with pin code or typical address tokens
    for line in lines:
        if re.search(r'\b\d{6}\b', line) or any(t in line for t in ['जिल', 'तालुका', 'Taluka', 'Dist', 'District']):
            return line.strip()

    return None
def get_birth_lines(text: str):
    lines = text.splitlines()
    return [line for line in lines if "जन्म" in line]
