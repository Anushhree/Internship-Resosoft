from PIL import Image, ImageEnhance, ImageOps
import numpy as np

def preprocess(file):
    # Load image with Pillow
    image = Image.open(file.file).convert("RGB")

    # Auto-orient (fix rotation based on EXIF metadata)
    image = ImageOps.exif_transpose(image)

    # Convert to grayscale
    gray = ImageOps.grayscale(image)

    # Enhance clarity (contrast)
    enhancer = ImageEnhance.Contrast(gray)
    enhanced = enhancer.enhance(1.5)

    # Convert back to numpy array for pytesseract
    return np.array(enhanced)