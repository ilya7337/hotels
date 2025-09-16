from datetime import date, datetime
from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2, room_id=2, date_from=date(2024, 6, 26), date_to=date(2024, 6, 30)
    )
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    new_booking = await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None
