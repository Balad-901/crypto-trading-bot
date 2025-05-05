# main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from dashboard.routes import router as dashboard_router
from startup import load_memory

app = FastAPI()

# Load memory on startup
memory = load_memory()

# CORS (optional for frontend integrations)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routes
app.include_router(api_router, prefix="/api")
app.include_router(dashboard_router)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
