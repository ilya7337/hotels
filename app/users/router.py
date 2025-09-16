from fastapi import APIRouter, Response, Depends
from app.users.dao import UsersDAO
from app.users.models import Users
from app.users.schemas import SUserAuth, SToken
from app.exceptions import (
    UserAlreadyExistsException,
    IncorectUserDataException,
)
from app.users.auth import (
    get_password,
    is_user_authenticate,
    create_access_token,
    create_refresh_token,
)
from app.users.dependencies import get_current_user


auth = APIRouter(prefix="/auth", tags=["Auth"])


@auth.post("/register")
async def register_user(user_data: SUserAuth):
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException
    hashed_password = get_password(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)


@auth.post("/login")
async def login_user(responce: Response, user_data: SUserAuth) -> SToken:
    user = await is_user_authenticate(user_data.email, user_data.password)
    if not user:
        raise IncorectUserDataException
    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    responce.set_cookie(
        "booking_access_token", access_token, httponly=True, secure=True, samesite="lax"
    )
    responce.set_cookie(
        "booking_refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    return SToken(access_token=access_token, refresh_token=refresh_token)


@auth.post("/logout")
async def logout(responce: Response):
    responce.delete_cookie("booking_access_token")
    responce.delete_cookie("booking_refresh_token")


@auth.get("/me")
async def me(user: Users = Depends(get_current_user)):
    return await UsersDAO.find_by_id(user.id)
