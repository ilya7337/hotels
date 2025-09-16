from pathlib import Path
import shutil
from fastapi import UploadFile
from app.hotels.rooms.models import Rooms
from app.images.models import RoomImages
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import insert


class RoomDAO(BaseDAO):
    model = Rooms

    @classmethod
    async def add(
        cls,
        name: str,
        hotel_id: int,
        description: str | None,
        price: int,
        services: list,
        quantity: int,
        images: list[UploadFile],
    ):
        async with async_session_maker() as session:

            room_data = {
                "name": name,
                "hotel_id": hotel_id,
                "description": description,
                "price": price,
                "services": services,
                "quantity": quantity,
            }
            room = await cls.add(room_data)

            upload_dir = Path("app/static/images/rooms") / str(room.id)
            upload_dir.mkdir(parents=True, exist_ok=True)

            for idx, image in enumerate(images):
                file_path = upload_dir / image.filename
                with file_path.open("wb") as buffer:
                    shutil.copyfileobj(image.file, buffer)

                image_url = f"/static/images/rooms/{room.id}/{image.filename}"
                image_data = {
                    "room_id": room.id,
                    "image_url": image_url,
                    "is_primary": idx == 0,  # Первое изображение считается основным
                }
                await session.execute(insert(RoomImages).values(**image_data))

            await session.commit()
            return room
        
    
