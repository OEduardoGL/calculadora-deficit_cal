# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import nutrition as nutrition_router
from app.api.v1.endpoints import auth as auth_router

from app.db.session import engine
from app.db.base import Base

from app.db.models import user as user_model  # noqa: F401
from app.db.models import calculation as calc_model  # noqa: F401

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(auth_router.router, prefix=settings.API_V1_PREFIX)
app.include_router(nutrition_router.router, prefix=settings.API_V1_PREFIX)

@app.get("/")
def root():
    return {"status": "ok", "name": settings.PROJECT_NAME}
