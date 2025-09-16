from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class HotelImages(Base):
    __tablename__ = "hotel_images"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    hotel_id = Column(
        Integer, ForeignKey("hotels.id", ondelete="CASCADE"), nullable=False
    )
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)

    hotel = relationship("Hotels", back_populates="images")


class RoomImages(Base):
    __tablename__ = "room_images"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True)
    room_id = Column(
        Integer, ForeignKey("rooms.id", ondelete="CASCADE"), nullable=False
    )
    image_url = Column(String, nullable=False)
    is_primary = Column(Boolean, default=False)
    room = relationship("Rooms", back_populates="images")
