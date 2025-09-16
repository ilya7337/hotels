from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from jose import jwt
from pydantic import EmailStr
from app.users.dao import UsersDAO
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password(password: str) -> str:
    return pwd_context.hash(password)


def verifiy_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode, settings.SECRET_JWT_KEY, algorithm=settings.ALGORITHM_JWT
    )


def create_refresh_token(data: dict):
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS
    )
    to_encode = data.copy()
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(
        to_encode, settings.SECRET_JWT_KEY, algorithm=settings.ALGORITHM_JWT
    )


async def is_user_authenticate(email: EmailStr, password: str):
    try:
        user = await UsersDAO.find_one_or_none(email=email)
        if not user or not verifiy_password(password, user.hashed_password):
            return None
        return user
    except Exception:
        return None


def verify_token(token: str):
    try:
        payload = jwt.decode(
            token=token, key=settings.SECRET_JWT_KEY, algorithms=settings.ALGORITHM_JWT
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None


def refresh_access_token(refresh_token: str):
    payload = verify_token(refresh_token)
    if not payload:
        return None

    if payload.get("type") != "refresh":
        return None

    new_access_token = create_access_token(data={"sub": payload["sub"]})
    return new_access_token
