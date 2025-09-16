import email
from email.message import EmailMessage
from pydantic import EmailStr
from app.config import settings


def create_booking_confirmation_template(booking: dict, email_to: EmailStr):
    email_message = EmailMessage()

    email_message["Subject"] = "Подтверждение бронирования"
    email_message["From"] = settings.SMPT_USER
    email_message["To"] = email_to

    email_message.set_content(
        f"""
        <h1>Подтвердите бронирование</h1>
        <div>Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}</div>
        """
    )
    return email_message
