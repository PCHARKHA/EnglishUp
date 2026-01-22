# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from app.db.base import Base  # For table creation
from app.db.session import engine  # Your DB engine
from app.api.v1.routers import analysis, auth, progress, evaluate, prompts  # Ensure all exist

# Lifespan event for startup/shutdown (replaces deprecated @app.on_event)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create DB tables
    Base.metadata.create_all(bind=engine)
    print("EnglishUp backend started - DB tables created")
    yield
    # Shutdown: Add cleanup if needed (e.g., close connections)
    print("EnglishUp backend shutting down")

# Create FastAPI app
app = FastAPI(
    title="EnglishUp API",
    version="1.0.0",
    description="Backend API for English speaking and writing evaluation",
    lifespan=lifespan  # Use lifespan instead of on_event
)

# Add CORS middleware (allow frontend origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-frontend-domain.com"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler for cleaner errors
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )

# Include routers (use aggregator if preferred: app.include_router(api_router, prefix="/api/v1"))
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"]
)
app.include_router(
    prompts.router,
    prefix="/api/v1/prompts",
    tags=["Prompts"]
)
app.include_router(
    evaluate.router,
    prefix="/api/v1/evaluate",
    tags=["Evaluation"]
)
app.include_router(
    analysis.router,
    prefix="/api/v1/analysis",
    tags=["Analysis"]
)
app.include_router(
    progress.router,
    prefix="/api/v1/progress",
    tags=["Progress"]
)

# Optional: Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to EnglishUp API"}