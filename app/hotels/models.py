from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    services = Column(JSON)
    rooms_quantity = Column(Integer)

    images = relationship(
        "HotelImages", back_populates="hotel", cascade="all, delete-orphan"
    )
    rooms = relationship("Rooms", back_populates="hotel", cascade="all, delete-orphan")

    def __str__(self):
        return self.name

