"""Unit tests for the Telegram API FastAPI microservice.

All Telegram API calls are mocked so the tests run without a real bot token.
"""

import os
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient
from telegram.error import TelegramError


os.environ["TELEGRAM_BOT_TOKEN"] = "fake-token-for-tests"


# Patch the Bot class before importing the FastAPI app, because the
# TelegramClient is created at module-import time.
with patch("telegram_api.utils.Bot") as _MockBot:
    _bot_instance = AsyncMock()
    _bot_instance.send_message = AsyncMock(
        return_value=AsyncMock(message_id=42)
    )
    _bot_instance.get_updates = AsyncMock(return_value=[])
    _bot_instance.shutdown = AsyncMock()
    _MockBot.return_value = _bot_instance

    from api.main import app


client = TestClient(app)


def _fake_update(update_id: int, chat_id: int, text: str = "Hi"):
    update = AsyncMock()
    update.update_id = update_id
    update.effective_chat = AsyncMock(id=chat_id)
    update.message = AsyncMock(text=text)
    return update


def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "telegram-api"}


def test_send_message():
    response = client.post(
        "/api/v1/send_message",
        json={"chat_id": 123456789, "text": "Hello!"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message_id"] == 42
    assert data["error"] is None


def test_send_message_empty_text():
    response = client.post(
        "/api/v1/send_message",
        json={"chat_id": 123456789, "text": ""},
    )
    assert response.status_code == 400
    assert "text" in response.json()["detail"].lower()


def test_send_reply_keyboard():
    response = client.post(
        "/api/v1/send_reply_keyboard",
        json={
            "chat_id": 123456789,
            "text": "Pick an option",
            "keyboard": [["Yes", "No"], ["Cancel"]],
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message_id"] == 42


def test_send_reply_keyboard_empty_keyboard():
    response = client.post(
        "/api/v1/send_reply_keyboard",
        json={"chat_id": 123456789, "text": "Pick", "keyboard": []},
    )
    assert response.status_code == 400


def test_remove_reply_keyboard():
    response = client.post(
        "/api/v1/remove_reply_keyboard",
        json={"chat_id": 123456789},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["message_id"] == 42


def test_get_updates():
    updates = [
        _fake_update(1, 123456789, "msg1"),
        _fake_update(2, 99999, "msg2"),
    ]
    with patch("telegram_api.utils.TelegramClient.get_updates") as mock_get:
        mock_get.return_value = updates
        response = client.post(
            "/api/v1/get_updates",
            json={"chat_id": 123456789, "limit": 10},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    # The endpoint delegates chat filtering to TelegramClient; since we mock
    # the class method, we get back the raw update list.
    assert len(data["updates"]) == 2
    assert data["updates"][0]["chat_id"] == 123456789
    assert data["updates"][0]["text"] == "msg1"
    mock_get.assert_awaited_once_with(chat_id=123456789, limit=10, timeout=0)


def test_get_chat_ids():
    updates = [
        _fake_update(1, 123456789, "msg1"),
        _fake_update(2, 123456789, "msg2"),
        _fake_update(3, 99999, "msg3"),
    ]
    with patch("telegram_api.utils.TelegramClient.get_updates") as mock_get:
        mock_get.return_value = updates
        response = client.get("/api/v1/get_chat_ids?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    chat_ids = [entry["chat_id"] for entry in data["chat_ids"]]
    assert chat_ids == [123456789, 99999]
    mock_get.assert_awaited_once_with(limit=10)


def test_error_handling():
    with patch("telegram_api.utils.TelegramClient.send_message") as mock_send:
        mock_send.side_effect = TelegramError("Telegram API failure")
        response = client.post(
            "/api/v1/send_message",
            json={"chat_id": 123456789, "text": "Hello!"},
        )
    assert response.status_code == 500
    assert "Telegram API failure" in response.json()["detail"]
