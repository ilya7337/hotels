from httpx import AsyncClient
import pytest


TEST_USER = {"email": "new_user@example.com", "password": "string"}


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("new_user@example.com", "string", 200),
        ("new_user@example.com", "string", 409),
        ("new_user", "string", 422),
        ("", "", 422),
    ],
)
async def test_register_user(email, password, status_code, ac: AsyncClient):
    responce = await ac.post(
        "/auth/register", json={"email": email, "password": password}
    )
    assert responce.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("user@example.com", "string", 200),
        ("error_user@example.com", "1234", 401),
        ("error_user", "1234", 422),
    ],
)
async def test_login_user(email, password, status_code, ac: AsyncClient):
    responce = await ac.post("/auth/login", json={"email": email, "password": password})
    assert responce.status_code == status_code


async def test_logout(ac: AsyncClient):
    await ac.post("/auth/login", json=TEST_USER)

    response = await ac.post("/auth/logout")
    assert response.status_code == 200

    cookies = response.cookies
    assert (
        "booking_access_token" not in cookies or cookies["booking_access_token"] == ""
    )
    assert (
        "booking_refresh_token" not in cookies or cookies["booking_refresh_token"] == ""
    )


@pytest.mark.asyncio
async def test_get_current_user(ac: AsyncClient):
    await ac.post("/auth/login", json=TEST_USER)

    response = await ac.get(
        "/auth/me", cookies={"booking_access_token": ac.cookies["booking_access_token"]}
    )
    assert response.status_code == 200

    user_data = response.json()
    assert user_data["email"] == TEST_USER["email"]

    await ac.post("/auth/logout")
    response = await ac.get("/auth/me")
    assert response.status_code == 401
