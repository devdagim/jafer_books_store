import logging

# aiogram
from aiogram import Router
from aiogram.types import ErrorEvent

error_router = Router(name="Route that not found")

@error_router.error()
async def error_handler(event: ErrorEvent):
    logging.critical("Critical error caused by %s", event.exception, exc_info=True)