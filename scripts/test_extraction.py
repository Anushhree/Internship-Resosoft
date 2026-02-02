from app.utils import ocr_engine
text = "नाव: राम\nजन्म तारीख 12 जानेवारी 1990\nजन्म वेळ 5:30 AM\nमोबाईल: +91 98765 43210\nईमेल: test.user@Example.COM"
print('extract_dob ->', ocr_engine.extract_dob(text))
print('extract_tob ->', ocr_engine.extract_tob(text))
print('format_tob ->', ocr_engine.format_tob_marathi(ocr_engine.extract_tob(text)))
print('format_dob ->', ocr_engine.format_dob_marathi(ocr_engine.extract_dob(text)))
