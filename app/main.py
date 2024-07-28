from fastapi import FastAPI
from app.routers import searches

app = FastAPI(title="Mock QRadar Ariel Search API", version="1.0.0")

app.include_router(searches.router)  # Include the searches router
