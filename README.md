## Hotels API — сервис бронирования (FastAPI)

Коротко: Backend‑сервис для бронирований отелей на FastAPI. Есть авторизация по JWT, разделы пользователей/отелей/комнат/бронирований, кэширование в Redis, админ‑панель на SQLAdmin, версионирование API.

### Стек
- **FastAPI**, **Uvicorn**
- **PostgreSQL** (через SQLAlchemy/engine), **Redis** (fastapi-cache)
- **SQLAdmin** (админка)
- **fastapi-versioning** (версионирование API)

### Быстрый старт
1) Установите зависимости
```bash
pip install -r requirements.txt
```

2) Настройте переменные окружения
Скопируйте пример и отредактируйте значения под вашу среду:
```bash
cp .env-example .env
```

3) Запустите приложение (локально)
```bash
uvicorn app.main:app --reload
```

- Откройте Swagger UI: `http://127.0.0.1:8000/v1/docs` (и/или `http://127.0.0.1:8000/docs`)
- Редок: `http://127.0.0.1:8000/v1/redoc`
- Админ‑панель SQLAdmin: `http://127.0.0.1:8000/admin`

> Подсказка: если видите ошибку вида `Error loading ASGI app. Attribute "app" not found in module "app"`, используйте правильный путь модуля: `uvicorn app.main:app --reload`.

### Что внутри
- Версионирование API: префиксы `/v{major}` (например, `/v1`)
- Кэш Redis: инициализация в lifespan, префикс `cache`
- Админка: `sqladmin.Admin`
- Статика: смонтирована на `/static`

### Структура проекта (упрощённо)
```text
app/
  main.py
  admin/
  bookings/
  hotels/
  pages/
  users/
  static/
```

### Переменные окружения
Базовый список находится в файле `.env-example`. Для локальной разработки можно также ориентироваться на `.env-non-dev`. 

### Разработка
- Горячая перезагрузка: `--reload`
- Запускайте Redis и PostgreSQL локально или через Docker, затем укажите корректные DSN в `.env`.



