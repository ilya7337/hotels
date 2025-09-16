from fastapi import APIRouter, File, UploadFile
from fastapi_versioning import version
from app.hotels.rooms.dao import RoomDAO
from app.hotels.rooms.schemas import SRooms, SRoomAdd

rooms = APIRouter(prefix="/{hotel_id}/rooms", tags=["Rooms"])


@rooms.get("")
@version(1)
async def get_rooms(hotel_id: int) -> list[SRooms]:
    return await RoomDAO.find_all(hotel_id=hotel_id)


@rooms.post("")
@version(1)
async def add_room(room_data: SRoomAdd, images: list[UploadFile] = File(...)):
    return await RoomDAO.add(
        name=room_data.name,
        hotel_id=room_data.hotel_id,
        description=room_data.description,
        price=room_data.price,
        services=room_data.services,
        quantity=room_data.quantity,
        images=images,
    )
