from pydantic import BaseModel
from typing import List
from fastapi import Form


class SHotels(BaseModel):
    id: int
    name: str
    location: str
    services: list
    rooms_quantity: int
    image_id: str


class HotelCreateForm:
    def __init__(
        self,
        name: str = Form(..., description="Название отеля", examples=["Grand Hotel"]),
        location: str = Form(..., description="Местоположение", examples=["Москва"]),
        services: str = Form(
            ..., description="Услуги (в формате JSON)", examples=["Wi-Fi, Бассейн"]
        ),
        rooms_quantity: int = Form(
            ..., description="Количество номеров", examples=[100]
        ),
    ):
        self.name = name
        self.location = location
        self.services = services
        self.rooms_quantity = rooms_quantity


class SHotelAdd(BaseModel):
    name: str
    location: str
    services: List[str]
    rooms_quantity: int
