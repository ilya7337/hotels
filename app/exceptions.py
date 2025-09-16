from fastapi import status, HTTPException

UserAlreadyExistsException = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Пользователь уже существует"
)

IncorectUserDataException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверные данные пользователя"
)


NullReTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Отсутствует токен"
)

InvalidTokenException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Невалидный токен"
)

TokenExpiredException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Токен истек"
)

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Не осталось свободных номеров/нет такой комнаты",
)


InvalidDateBooking = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="День заезда и выезда должны отличаться",
)

InvalidDateBooking2 = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="День заезда должен быть раньше выезда"
)

InvalidJsonFormat = HTTPException(status_code=422, detail="Неверный JSON формат")
