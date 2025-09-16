from csv import DictReader
import json
from datetime import datetime
from typing import Dict, Any


def convert_row(model: str, row: Dict[str, Any]) -> Dict[str, Any]:
    """Преобразует типы данных в строке CSV в соответствии с моделью"""
    type_conversions = {
        "hotels": {
            "id": int,
            "rooms_quantity": int,
            "services": lambda x: json.loads(x.replace("'", '"')),
        },
        "rooms": {
            "id": int,
            "hotel_id": int,
            "price": int,
            "quantity": int,
            "services": lambda x: json.loads(x.replace("'", '"')),
        },
        "bookings": {
            "id": int,
            "user_id": int,
            "room_id": int,
            "price": int,
            "date_from": lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
            "date_to": lambda x: datetime.strptime(x, "%Y-%m-%d").date(),
        },
        "users": {"id": int},
    }

    conversions = type_conversions.get(model, {})
    for field, convert in conversions.items():
        if field in row and row[field]:
            try:
                row[field] = convert(row[field])
            except (ValueError, json.JSONDecodeError) as e:
                raise e

    return row


def open_mock_csv(model: str) -> list[Dict[str, Any]]:
    """Загружает данные из CSV с автоматическим преобразованием типов"""
    with open(f"app/tests/mock_{model}.csv", "r", encoding="utf-8") as file:
        reader = DictReader(file)
        return [convert_row(model, row) for row in reader if any(row.values())]
