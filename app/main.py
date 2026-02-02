from fastapi import FastAPI
from app.database import init_db
from app.routers import ocr_routes

app = FastAPI(title="Marathi Biodata OCR API")
init_db()
# Register OCR routes
app.include_router(ocr_routes.router)


# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to Marathi Biodata OCR API"}