from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

img = Image.open(r"C:\Users\Anushree\OneDrive\Desktop\Anushree AM2140\image 1.png") # replace with your biodata image
text = pytesseract.image_to_string(img, lang="mar")
print(text)