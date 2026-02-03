from fastapi import FastAPI
from app.database import init_db
from app.routers import generate, images

app = FastAPI(title="Image Generator API")

@app.on_event("startup")
def startup_event():
    init_db()


@app.get("/")
def read_root():
    return {"message": "Image Generator API", "docs": "/docs"}

app.include_router(generate.router)
app.include_router(images.router)