from app.logger import logger
from app.bookings.models import Bookings
from app.dao.base import BaseDAO
from datetime import date
from sqlalchemy import and_, or_, select, func, insert
from sqlalchemy.exc import SQLAlchemyError
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker

class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        try:
            async with async_session_maker() as session:
                room_exists = await session.execute(
                    select(Rooms).where(Rooms.id == room_id)
                )
                if not room_exists.scalar():
                    return None

                booked_rooms = (
                    select(Bookings)
                    .where(
                        and_(
                            Bookings.room_id == room_id,
                            or_(
                                and_(
                                    Bookings.date_from >= date_from,
                                    Bookings.date_from <= date_to,
                                ),
                                and_(
                                    Bookings.date_from <= date_from,
                                    Bookings.date_to > date_from,
                                ),
                            ),
                        )
                    )
                    .cte("booked_rooms")
                )
                rooms_left = (
                    select(Rooms.quantity - func.count(booked_rooms.c.room_id))
                    .select_from(Rooms)
                    .join(booked_rooms, booked_rooms.c.room_id == Rooms.id)
                    .where(Rooms.id == room_id)
                    .group_by(Rooms.quantity, booked_rooms.c.room_id)
                )
                get_cnt_left_rooms = await session.execute(rooms_left)
                cnt_left_rooms: int = get_cnt_left_rooms.scalar()
                if not cnt_left_rooms or cnt_left_rooms > 0:
                    get_price = select(Rooms.price).filter_by(id=room_id)
                    price = await session.execute(get_price)
                    price: int = price.scalar()
                    add_booking = (
                        insert(Bookings)
                        .values(
                            room_id=room_id,
                            user_id=user_id,
                            date_from=date_from,
                            date_to=date_to,
                            price=price,
                        )
                        .returning(Bookings)
                    )

                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                else:
                    None
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                exc_msg = "Database Exc"
            elif isinstance(e, Exception):
                exc_msg = "Unknow Exc"
            exc_msg += ": Cannot add booking"
            extra = {
                "room_id": room_id,
                "user_id": user_id,
                "date_from": date_from,
                "date_to": date_to,
            }
            logger.error(exc_msg, extra=extra, exc_info=True)
