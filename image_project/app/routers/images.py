from fastapi import APIRouter
from app.database import get_db_connection

router = APIRouter(prefix="/images", tags=["Images"])

@router.get("/{id}")
def get_image(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT prompt, filepath FROM images WHERE id=?", (id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"prompt": row[0], "filepath": row[1]}
    return {"error": "Image not found"}