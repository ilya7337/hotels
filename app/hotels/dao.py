from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile
from app.hotels.models import Hotels
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from app.images.models import HotelImages
from app.tasks.tasks import process_image
from app.logger import logger


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def add(
        cls,
        name: str,
        location: str,
        services: list,
        rooms_quantity: int,
        images: list[UploadFile],
    ):
        try:
            async with async_session_maker() as session:
                # Создаем отель
                hotel_query = (
                    insert(Hotels)
                    .values(
                        name=name,
                        location=location,
                        services=services,
                        rooms_quantity=rooms_quantity,
                    )
                    .returning(Hotels)
                )
                hotel = await session.execute(hotel_query)
                hotel = hotel.scalar()
                await session.commit()

                # Создаем директорию для изображений
                upload_dir = Path("app/static/images/hotels") / str(hotel.id)
                upload_dir.mkdir(parents=True, exist_ok=True)

                image_urls = []
                for idx, image in enumerate(images):
                    try:
                        # Сохраняем оригинальное изображение
                        file_name = f"{uuid4()}.webp"
                        image_path = upload_dir / file_name
                        image_url = f"/static/images/hotels/{hotel.id}/{file_name}"

                        # Читаем и сохраняем оригинальное изображение
                        image_content = await image.read()
                        with open(image_path, "wb") as buffer:
                            buffer.write(image_content)

                        # Отправляем задачу на оптимизацию изображения
                        process_image.delay(
                            original_image_path=str(image_path),
                            quality=80,  # можно настроить качество
                            max_size=(1920, 1080),  # максимальный размер
                        )

                        image_urls.append(image_url)
                        await image.seek(0)

                        # Сохраняем запись об изображении в БД
                        await session.execute(
                            insert(HotelImages).values(
                                hotel_id=hotel.id,
                                image_url=image_url,
                                is_primary=idx == 0,
                            )
                        )

                    except Exception as e:
                        logger.error(f"Error processing image {idx}: {str(e)}", exc_info=True)
                        continue

                await session.commit()
                return hotel
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                exc_msg = "Database Exc"
            elif isinstance(e, Exception):
                exc_msg = "Unknow Exc"
            exc_msg += f": Cannot add hotel"
            extra = {
                "name": name,
                "location": location,
            }
            logger.error(exc_msg, extra=extra, exc_info=True)
    

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Ищет все запись отелей базе данных по заданным критериям с предзагрузкой фото
        """
        try:
            async with async_session_maker() as session:
                query = select(Hotels).options(joinedload(Hotels.images)).filter_by(**filter_by)
                all_records = await session.execute(query)
                return all_records.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                exc_msg = "Database Exc"
            elif isinstance(e, Exception):
                exc_msg = "Unknow Exc"
            exc_msg += f": Cannot find {cls.model}"
            extra = {
                **filter_by
            }
            logger.error(exc_msg, extra=extra, exc_info=True)
            