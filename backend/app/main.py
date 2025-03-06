import os

from fastapi import Depends, FastAPI
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="Maeni")

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/maeni")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"message": "前に進む"}


@app.get("/health")
def health_check(db=Depends(get_db)):
    try:
        # Execute a simple query to check database connection
        result = db.execute(text("SELECT 1")).scalar()
        return {
            "status": "healthy",
            "database": "connected" if result == 1 else "error",
        }
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}
