import os

import pytest
from fastapi.testclient import TestClient

os.environ.setdefault("APP_POSTGRES_URL", "postgresql+asyncpg://app:app@postgres:5432/app")
os.environ.setdefault("APP_MONGO_URL", "mongodb://mongo:27017")
os.environ.setdefault("APP_MONGO_DB", "app")


@pytest.fixture
def client():
    from app.main import app
    with TestClient(app) as c:
        yield c
