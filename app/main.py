# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.db.base import Base
from app.db.session import engine

from app.api.v1.routers import analysis, auth, progress, evaluate, prompts


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup / shutdown lifecycle.
    NOTE: create_all is acceptable for MVP only.
    """
    Base.metadata.create_all(bind=engine)
    print("✅ EnglishUp backend started")
    yield
    print("🛑 EnglishUp backend shutting down")


app = FastAPI(
    title="EnglishUp API",
    version="1.0.0",
    description="Backend API for English speaking and writing evaluation",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-frontend-domain.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Safer global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"🔥 Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Register routers
# IMPORTANT: routers already define their own prefixes
app.include_router(auth.router)
app.include_router(prompts.router)
app.include_router(evaluate.router)
app.include_router(analysis.router)
app.include_router(progress.router)

@app.get("/")
def root():
    return {"message": "Welcome to EnglishUp API"}
