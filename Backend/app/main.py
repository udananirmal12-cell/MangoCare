from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router
from app.api.profile import router as profile_router



from app.api.leaf import (
    router as leaf_router
)

from app.api.fruit import (
    router as fruit_router
)

from app.api.advisory import (
    router as advisory_router
)

from app.api.history import (
    router as history_router
)

from app.api.weather import (
    router as weather_router
)


app = FastAPI(
    title="MangoCare API",
    description=(
        "Backend API for the AI-Powered "
        "Mango Cultivation Management System"
    ),
    version="1.0.0"
)

# Railway frontend CORS enabled
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://mangocare.up.railway.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# --------------------------------------------------
# Routers
# --------------------------------------------------

app.include_router(
    leaf_router
)

app.include_router(
    fruit_router
)

app.include_router(
    advisory_router
)

app.include_router(auth_router)
app.include_router(profile_router)


# --------------------------------------------------
# Uploaded images
# --------------------------------------------------

app.mount(
    "/uploads",
    StaticFiles(
        directory="uploads"
    ),
    name="uploads"
)


# --------------------------------------------------
# Basic endpoints
# --------------------------------------------------

@app.get("/")
def root():

    return {
        "application": "MangoCare",
        "message": "MangoCare backend is running"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }

app.include_router(
    history_router
)

app.include_router(
    weather_router
)