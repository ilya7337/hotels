from tkinter import NO
from fastapi import Request, Depends, Response
from app.users.dao import UsersDAO
from app.users.auth import refresh_access_token, verify_token, create_access_token
from datetime import datetime, timezone
from app.config import settings
from app.exceptions import InvalidTokenException


def get_access_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise InvalidTokenException
    return token


def get_refresh_token(request: Request):
    token = request.cookies.get("booking_refresh_token")
    if not token:
        return None
    return token


async def get_current_user(
    response: Response,
    access_token: str = Depends(get_access_token),
    refresh_token: str = Depends(get_refresh_token),
):

    payload_access = verify_token(access_token)
    if not payload_access and refresh_token:
        payload_refresh = verify_token(refresh_token)

        if payload_refresh:
            new_token = refresh_access_token(refresh_token)
            user_id = payload_refresh.get("sub")
            if new_token:
                response.set_cookie(
                    key="booking_access_token",
                    value=create_access_token({"sub": user_id}),
                    httponly=True,
                    secure=True,
                    samesite="lax",
                )
            else:
                raise InvalidTokenException
    else:
        user_id: str = payload_access.get("sub")

    if not user_id:
        raise InvalidTokenException

    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise InvalidTokenException

    return user
