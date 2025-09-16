from pydantic import EmailStr
from app.config import settings
from app.tasks.celery import celery_app
from PIL import Image

from pathlib import Path
from smtplib import SMTP_SSL, SMTPAuthenticationError, SMTPConnectError, SMTPDataError
from app.tasks.email_templates import create_booking_confirmation_template

from app.logger import logger

@celery_app.task(bind=True)
def process_image(
    self, original_image_path: str, quality: int = 80, max_size: tuple = (1920, 1080)
):
    try:
        original_path = Path(original_image_path)
        if not original_path.exists():
            raise FileNotFoundError(f"Image file not found: {original_image_path}")

        with Image.open(original_path) as img:
            img.thumbnail(max_size, Image.LANCZOS)

            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            img.save(
                original_path, format="WEBP", quality=quality, optimize=True, method=6
            )

        return f"Image {original_image_path} optimized successfully"

    except Exception as e:
        # Удаляем поврежденный файл, если что-то пошло не так
        if original_path.exists():
            original_path.unlink()
        self.retry(exc=e)


@celery_app.task
def send_booking_conformation_email(booking: dict, email_to: EmailStr):
    try:
        msg_content = create_booking_confirmation_template(booking, email_to)
        with SMTP_SSL(settings.SMPT_HOST, settings.SMPT_PORT) as server:
            server.login(settings.SMPT_USER, settings.SMTP_PASS)
            server.send_message(msg_content)
    except (SMTPAuthenticationError, SMTPConnectError, SMTPDataError, Exception)  as e:
        if isinstance(e, SMTPAuthenticationError):
            exc_msg = "Authentication error"
        elif isinstance(e, SMTPConnectError):
            exc_msg = "Connection error"
        elif isinstance(e, SMTPDataError):
            exc_msg = "Data transmission error"
        else:
            exc_msg = "Unknown error"

        extra = {
            "booking_id": booking["id"],    
            "email_to": email_to
        }

        logger.error(f"{exc_msg}: Failed to send confirmation email.", extra=extra, exc_info=True)
        raise e
