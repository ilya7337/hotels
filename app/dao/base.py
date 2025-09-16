from pyexpat import model
from app.database import async_session_maker
from sqlalchemy import select, insert, delete
from sqlalchemy.exc import SQLAlchemyError
from app.logger import logger


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        """
        Ищет запись в базе данных по id элемента
        """
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(id=model_id)
                res = await session.execute(query)
                return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                exc_msg = "Database Exc"
            elif isinstance(e, Exception):
                exc_msg = "Unknow Exc"
            exc_msg += f": Cannot find {cls.model}"
            extra = {
                "id": model_id,
            }
            logger.error(exc_msg, extra=extra, exc_info=True)

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        """
        Ищет одну конкретную запись
        """
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)
                res = await session.execute(query)
                return res.scalar_one_or_none()
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

    @classmethod
    async def find_all(cls, **filter_by):
        """
        Ищет все запись в базе данных по заданным критериям
        """
        try:
            async with async_session_maker() as session:
                query = select(cls.model).filter_by(**filter_by)
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

    @classmethod
    async def add(cls, **data):
        """
        Добавляет запись в базу данных
        """
        try:
            async with async_session_maker() as session:
                query = insert(cls.model).values(**data).returning(cls.model)
                result = await session.execute(query)
                await session.commit()
                return result.scalars().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                exc_msg = "Database Exc"
            elif isinstance(e, Exception):
                exc_msg = "Unknow Exc"
            exc_msg += f": Cannot add {cls.model}"
            logger.error(exc_msg, exc_info=True)
    
    @classmethod
    async def delete(cls, **filters):
        """
        Удаляет запись из базы данных по заданным критериям фильтров
        """
        try:
            async with async_session_maker() as session:
                query = delete(cls.model).filter_by(**filters)
                result = await session.execute(query)
                await session.commit()
                return result.rowcount
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                exc_msg = "Database Exc"
            elif isinstance(e, Exception):
                exc_msg = "Unknow Exc"
            exc_msg += f": Cannot delete from {cls.model.__tablename__}"
            logger.error(exc_msg, exc_info=True)
        raise e
