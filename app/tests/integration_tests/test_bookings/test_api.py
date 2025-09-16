import pytest
from httpx import AsyncClient


@pytest.mark.parametrize(
    "room_id,date_from,date_to,status",
    [
        (10, "2024-06-26", "2024-06-30", 200),
        (10, "2024-06-26", "2024-06-30", 200),
        (10, "2024-06-26", "2024-06-30", 200),
        (10, "2024-06-26", "2024-06-30", 409),
    ],
)
async def test_add_and_get_booking(
    room_id, date_from, date_to, status, auth_user: AsyncClient
):
    assert "booking_access_token" in auth_user.cookies
    responce = await auth_user.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
        cookies={"booking_access_token": auth_user.cookies["booking_access_token"]},
    )
    assert responce.status_code == status


async def test_get_bookings(auth_user: AsyncClient):
    response = await auth_user.get(
        "/bookings",
        cookies={"booking_access_token": auth_user.cookies["booking_access_token"]},
    )
    assert response.status_code == 200
    if response.status_code == 200:
        assert isinstance(response.json(), list)


@pytest.mark.parametrize(
    "room_id,date_from,date_to,status,error",
    [
        (
            10,
            "2024-06-30",
            "2024-06-30",
            409,
            "День заезда и выезда должны отличаться",
        ),
        (
            10,
            "2024-06-30",
            "2024-06-26",
            409,
            "День заезда должен быть раньше выезда",
        ),
    ],
)
async def test_booking_date_validation(
    room_id, date_from, date_to, status, error, auth_user: AsyncClient
):
    response = await auth_user.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
        cookies={"booking_access_token": auth_user.cookies["booking_access_token"]},
    )
    assert response.status_code == status
    assert error in response.json()["detail"]


async def test_get_bookings_unauthorized(ac: AsyncClient):
    response = await ac.get("/bookings")
    assert response.status_code == 401


async def test_booking_response_format(auth_user: AsyncClient):
    response = await auth_user.post(
        "/bookings",
        json={"room_id": 10, "date_from": "2024-07-01", "date_to": "2024-07-05"},
        cookies={"booking_access_token": auth_user.cookies["booking_access_token"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "room_id" in data
    assert "user_id" in data
    assert "date_from" in data
    assert "date_to" in data
    assert "price" in data
    assert "total_cost" in data
    assert "total_days" in data


@pytest.mark.parametrize(
    "room_id,date_from,date_to,status",
    [
        (10, "2024-06-30", "2024-17-01", 422),
        (10, "2024-06-30", "2024-07-31", 200),
    ],
)
async def test_edge_cases(room_id, date_from, date_to, status, auth_user: AsyncClient):
    response = await auth_user.post(
        "/bookings",
        json={"room_id": room_id, "date_from": date_from, "date_to": date_to},
        cookies={"booking_access_token": auth_user.cookies["booking_access_token"]},
    )
    assert response.status_code == status
