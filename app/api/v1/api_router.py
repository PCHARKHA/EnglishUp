# app/api/v1/routers/__init__.py
from fastapi import APIRouter
from app.api.v1.routers import auth, prompts, analysis, progress, evaluate  
# Create a central router for all v1 endpoints
api_router = APIRouter()

# Include sub-routers with consistent prefixes (relative to /api/v1)
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(prompts.router, prefix="/prompts", tags=["prompts"])
api_router.include_router(evaluate.router, prefix="/evaluate", tags=["evaluate"])  # Added
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(progress.router, prefix="/progress", tags=["progress"])

# Optional: Add a simple health check endpoint
@api_router.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "message": "EnglishUp API is running"}
