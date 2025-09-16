import email
import pytest
from app.users.dao import UsersDAO
from app.users.models import Users
from app.users.schemas import SUserAuth

TEST_USER = {"email": "testuser@example.com", "hashed_password": "test_password"}


async def test_add_and_get_user():
    new_user = await UsersDAO.add(
        email=TEST_USER["email"], hashed_password=TEST_USER["hashed_password"]
    )
    assert new_user.email == TEST_USER["email"]
    assert new_user.hashed_password == TEST_USER["hashed_password"]

    found_user = await UsersDAO.find_by_id(new_user.id)
    assert found_user is not None
    assert found_user.email == TEST_USER["email"]


async def test_find_one_or_none():
    await UsersDAO.add(email="qwe@mail.ru", hashed_password="1234")
    user = await UsersDAO.find_one_or_none(email="qwe@mail.ru")
    assert user is not None
    assert user.email == "qwe@mail.ru"

    user = await UsersDAO.find_one_or_none(email="nonexistent@example.com")
    assert user is None
