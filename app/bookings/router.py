from fastapi import APIRouter, Depends
from pydantic import TypeAdapter
from app.bookings.dao import BookingDAO
from app.bookings.schemas import SBooking, SBookingAdd
from app.tasks.tasks import send_booking_conformation_email
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exceptions import InvalidDateBooking, InvalidDateBooking2, RoomCannotBeBooked


booking = APIRouter(prefix="/bookings", tags=["Бронирования"])


@booking.get("")
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)


@booking.post("")
async def add_booking(
    booking_data: SBookingAdd, user: Users = Depends(get_current_user)
):
    if booking_data.date_from == booking_data.date_to:
        raise InvalidDateBooking
    if booking_data.date_from > booking_data.date_to:
        raise InvalidDateBooking2
    booking = await BookingDAO.add(
        user.id, booking_data.room_id, booking_data.date_from, booking_data.date_to
    )
    if not booking:
        raise RoomCannotBeBooked
    adapter = TypeAdapter(SBooking)
    booking_dict = adapter.validate_python(booking).model_dump()
    send_booking_conformation_email.delay(booking_dict, user.email)
    return booking
