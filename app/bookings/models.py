from app.database import Base
from sqlalchemy import Column, Integer, ForeignKey, Date, Computed
from sqlalchemy.orm import relationship


class Bookings(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    room_id = Column(ForeignKey("rooms.id"))
    user_id = Column(ForeignKey("users.id"))
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("(date_to - date_from) * price"))
    total_days = Column(Integer, Computed("date_to - date_from"))

    user = relationship("Users", back_populates="bookings")
    room = relationship("Rooms", back_populates="booking")

    def __str__(self):
        return f"Бронь {self.id}"
