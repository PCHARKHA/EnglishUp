from fastapi import FastAPI
from app.api.v1.routers import analysis, auth, progress, evaluate, prompts


# Create FastAPI app (GENERIC)
app = FastAPI(
    title="EnglishUp API",
    version="1.0.0",
    description="Backend API for English speaking and writing evaluation"
)

# Include routers (GENERIC mechanism, EnglishUp meaning)
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

# Startup event (optional but clean)
@app.on_event("startup")
def on_startup():
    print("EnglishUp backend started")