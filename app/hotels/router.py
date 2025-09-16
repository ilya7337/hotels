from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from app.hotels.dao import HotelDAO
from app.hotels.schemas import SHotels, SHotelAdd, HotelCreateForm
from app.hotels.rooms.router import rooms
from fastapi_cache.decorator import cache
import json
from typing import List
from fastapi_versioning import version

hotels = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)
hotels.include_router(rooms)


@hotels.get("")
@version(1)
@cache(expire=30)
async def get_hotels() -> list[SHotels]:
    return await HotelDAO.find_all()


@hotels.post("/")
@version(1)
async def add_hotel(
    form_data: HotelCreateForm = Depends(),
    images: List[UploadFile] = File(..., description="Фотографии отеля"),
):
    try:
        # Валидируем данные через Pydantic
        hotel_data = SHotelAdd(
            name=form_data.name,
            location=form_data.location,
            services=form_data.services.split(", "),
            rooms_quantity=form_data.rooms_quantity,
        )

        return await HotelDAO.add(**hotel_data.dict(), images=images)

    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Неверный формат услуг")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
