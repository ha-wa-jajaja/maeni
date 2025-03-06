from app.database import Base, engine
from app.routers import user
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create tables (in development; use Alembic for migrations in production)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Maeni Learning API",
    description="API for the Maeni Learning application",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user.router)


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
