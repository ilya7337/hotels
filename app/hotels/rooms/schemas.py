from pydantic import BaseModel
from typing import Optional, List


class SRooms(BaseModel):
    id: int
    hotel_id: int
    name: str
    description: str
    price: int
    services: list
    quantity: int
    image_id: int


class SRoomAdd(BaseModel):
    name: str
    hotel_id: int
    description: Optional[str] = None
    price: int
    services: List[str]
    quantity: int
