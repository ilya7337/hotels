from time import time
from fastapi import Request
from app.main import app
from app.logger import logger


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time()
    responce = await call_next(request)
    process_time = time() - start_time
    logger.info(
        "Request handling time", 
        extra={
            "process_time": round(process_time, 4)
        }
    )
    return responce