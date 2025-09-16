from sqlalchemy import insert
from app.bookings.models import Bookings
from app.config import settings
from app.database import engine, async_session_maker, Base

from pytest import fixture

from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users

from httpx import AsyncClient

from app.main import app as fastapi_app

from data_handler import open_mock_csv


@fixture(autouse=True, scope="module")
async def prepare_database():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    try:
        hotels = open_mock_csv("hotels")
        rooms = open_mock_csv("rooms")
        users = open_mock_csv("users")
        bookings = open_mock_csv("bookings")

    except Exception as e:
        raise e

    async with async_session_maker() as session:
        try:
            if hotels:
                await session.execute(insert(Hotels).values(hotels))
            if rooms:
                await session.execute(insert(Rooms).values(rooms))
            if users:
                await session.execute(insert(Users).values(users))
            if bookings:
                await session.execute(insert(Bookings).values(bookings))

            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


# Для асинхронных тестов
@fixture(scope="function")
async def ac():
    """Async Client"""
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        yield client


@fixture(scope="function")
async def session():
    async with async_session_maker() as session:
        yield session


@fixture(scope="session")
async def auth_user():
    """Auth async client"""
    async with AsyncClient(app=fastapi_app, base_url="http://test") as client:
        await client.post(
            "/auth/login", json={"email": "akhtyamov_ilya@mail.ru", "password": "1234"}
        )  # user_id 5
        assert client.cookies["booking_access_token"]
        yield client
