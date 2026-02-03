from fastapi import FastAPI
from database import init_db
from routers import coordinates

app = FastAPI()

# Initialize DB
init_db()

# Include routers
app.include_router(coordinates.router)