from fastapi import APIRouter
from app.models import PromptRequest
from app.database import get_db_connection
from app.image_generator import generate_image
import os
from datetime import datetime

router = APIRouter(prefix="/generate", tags=["Generate"])

SAVE_DIR = "generated_images"
os.makedirs(SAVE_DIR, exist_ok=True)

@router.post("/")
def generate(req: PromptRequest):
    image = generate_image(req.prompt)

    # Unique filename based on timestamp
    filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(SAVE_DIR, filename)

    # Save image to disk
    image.save(filepath)

    # Store prompt + filepath in DB
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO images (prompt, filepath) VALUES (?, ?)", (req.prompt, filepath))
    conn.commit()
    conn.close()

    return {"message": "Image generated and stored successfully", "filepath": filepath}