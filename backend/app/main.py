from fastapi import FastAPI

from app.database import test_connection
from app.routes.student_routes import router as student_router

app = FastAPI(
    title="SkillSync API",
    description="Student Skills and Internship Platform",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to SkillSync API"
    }


@app.get("/health")
def health():
    try:
        test_connection()

        return {
            "status": "healthy",
            "database": "MongoDB connected"
        }

    except Exception:
        return {
            "status": "unhealthy"
        }


app.include_router(student_router)