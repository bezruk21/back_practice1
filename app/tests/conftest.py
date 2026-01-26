import pytest
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from httpx import AsyncClient, ASGITransport
from app.app import app
from app.config import CONFIG
from app.models.user import User
from app.models.animal_card import AnimalCard


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def init_test_db():
    client = AsyncIOMotorClient(CONFIG.mongo_uri)
    test_db = client["test_practice_db"]
    app.db = test_db

    await init_beanie(database=app.db, document_models=[User, AnimalCard])
    yield
    await client.drop_database("test_practice_db")


@pytest.fixture
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client