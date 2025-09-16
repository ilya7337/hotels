from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from app.hotels.router import get_hotels


pages = APIRouter(prefix="/pages", tags=["Frontend"])

templates = Jinja2Templates(directory="app/templates")


@pages.get("/hotels")
async def register_user(request: Request, hotels=Depends(get_hotels)):
    return templates.TemplateResponse(
        name="hotels.html", context={"request": request, "hotels": hotels}
    )
