import asyncio
import os
import pytest
import httpx
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db.base import Base
from app.api import deps

TEST_DATABASE_URL = "sqlite+pysqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(autouse=True)
def override_settings_env(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "tests-secret-key")
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60")
    monkeypatch.setenv("BACKEND_CORS_ORIGINS", "http://localhost:3000,http://localhost:5173")

@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(autouse=True)
def _override_get_db(db_session):
    def _get_db():
        try:
            yield db_session
        finally:
            pass

    deps.get_db = _get_db  
    app.dependency_overrides[deps.get_db] = _get_db
    yield
    app.dependency_overrides.pop(deps.get_db, None)

@pytest.fixture
async def client():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
