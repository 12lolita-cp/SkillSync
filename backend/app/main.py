
from fastapi import FastAPI

from app.routes.auth_routes import router as auth_router
from app.routes.student_routes import router as student_router
from app.routes.skill_routes import router as skill_router
from app.routes.certification_routes import router as certification_router
from app.routes.internship_routes import router as internship_router
from app.routes.application_routes import router as application_router


app = FastAPI(
    title="SkillSync API",
    description="Student Skills, Projects and Internship Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {"message": "SkillSync API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


# Register API routers
app.include_router(student_router)
app.include_router(skill_router)
app.include_router(certification_router)
app.include_router(internship_router)
app.include_router(auth_router)
app.include_router(application_router)
