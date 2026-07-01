"""FastAPI entry point for the Telegram API microservice."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from telegram_api import TelegramClient

from .router import create_router


# Initialize the Telegram client once at import time. The token is validated
# immediately, so the service fails fast if it is misconfigured.
_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
if not _BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required.")
_client = TelegramClient(token=_BOT_TOKEN)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Yield control to the app and shut down the client on exit."""
    yield
    await _client.shutdown()


app = FastAPI(
    title="Telegram API Microservice",
    description="HTTP wrapper around the Telegram Bot API.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "service": "telegram-api"}


app.include_router(create_router(_client))
