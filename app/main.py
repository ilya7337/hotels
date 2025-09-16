from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from fastapi_versioning import VersionedFastAPI

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import booking
from app.config import settings
from app.database import engine
from app.hotels.router import hotels
from app.pages.router import pages
from app.users.router import auth


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(
        settings.REDIS_URL, encoding="utf8", decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    await redis.close()


app = FastAPI(lifespan=lifespan)


app.include_router(auth)
app.include_router(booking)
app.include_router(pages)
app.include_router(hotels)


app = VersionedFastAPI(app, 
    version_format="{major}",
    prefix_format="/v{major}"                      
)
    

admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
app.mount("/static", StaticFiles(directory="app/static"), "static")