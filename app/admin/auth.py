from operator import setitem
from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from app.config import settings

from app.exceptions import IncorectUserDataException
from app.users.auth import (
    create_access_token,
    create_refresh_token,
    is_user_authenticate,
    verify_token,
)


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await is_user_authenticate(email, password)
        if user and user.role == "admin":
            access_token = create_access_token({"sub": str(user.id)})
            refresh_token = create_refresh_token({"sub": str(user.id)})
            request.session.update({"a_token": access_token, "r_token": refresh_token})
            return True
        return RedirectResponse(request.url_for("admin:login"), status_code=302)

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("a_token")

        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        if verify_token(token):
            return True
        return RedirectResponse(request.url_for("admin:login"), status_code=302)


authentication_backend = AdminAuth(secret_key=settings.SECRET_JWT_KEY)
