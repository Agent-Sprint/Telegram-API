"""Small test script for the Telegram API wrapper.

Set TELEGRAM_BOT_TOKEN to run against the real Telegram API, otherwise the
script runs a quick mock-only smoke test.
"""

import asyncio
import logging
import os
from unittest.mock import AsyncMock, patch

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update

from telegram_api import TelegramClient

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

OFFSET_PATH = ".telegram_offset"


def _fake_update(update_id: int, chat_id: int) -> Update:
    update = AsyncMock(spec=Update)
    update.update_id = update_id
    update.effective_chat = AsyncMock(id=chat_id)
    return update


async def _test_mock() -> None:
    logger.info("Running mock smoke test")

    fake_update_1 = _fake_update(1, chat_id=12345)
    fake_update_2 = _fake_update(2, chat_id=12345)
    fake_update_3 = _fake_update(3, chat_id=99999)

    with patch("telegram_api.utils.Bot") as MockBot:
        bot_instance = AsyncMock()
        bot_instance.send_message = AsyncMock(return_value=AsyncMock(message_id=42))
        bot_instance.get_updates = AsyncMock(
            return_value=[fake_update_1, fake_update_2, fake_update_3]
        )
        MockBot.return_value = bot_instance

        client = TelegramClient(token="fake-token", offset_path=None)

        sent = await client.send_message(
            chat_id=12345, text="Hello from the mock test"
        )
        assert sent.message_id == 42
        bot_instance.send_message.assert_awaited_once_with(
            chat_id=12345, text="Hello from the mock test"
        )
        logger.info("send_message passed")

        keyboard = [["Yes", "No"], ["Cancel"]]
        sent = await client.send_reply_keyboard(
            chat_id=12345, text="Pick an option", keyboard=keyboard
        )
        assert sent.message_id == 42
        call = bot_instance.send_message.call_args
        assert call.kwargs["chat_id"] == 12345
        assert call.kwargs["text"] == "Pick an option"
        reply_markup = call.kwargs["reply_markup"]
        assert isinstance(reply_markup, ReplyKeyboardMarkup)
        button_texts = [[btn.text for btn in row] for row in reply_markup.keyboard]
        assert button_texts == keyboard
        logger.info("send_reply_keyboard passed")

        sent = await client.remove_reply_keyboard(chat_id=12345)
        assert sent.message_id == 42
        call = bot_instance.send_message.call_args
        assert call.kwargs["chat_id"] == 12345
        assert call.kwargs["text"] == "Keyboard removed."
        assert isinstance(call.kwargs["reply_markup"], ReplyKeyboardRemove)
        logger.info("remove_reply_keyboard passed")

        all_updates = await client.get_updates(limit=10)
        assert len(all_updates) == 3

        by_chat = await client.get_updates(chat_id=12345)
        assert len(by_chat) == 2
        assert {u.update_id for u in by_chat} == {1, 2}

        logger.info("get_updates passed")


async def _test_real() -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = int(os.environ.get("TELEGRAM_CHAT_ID", "0") or 0)

    if not chat_id:
        raise ValueError(
            "For a real test, set the TELEGRAM_CHAT_ID environment variable."
        )

    client = TelegramClient(token=token, offset_path=OFFSET_PATH)
    try:
        logger.info("Sending a reply keyboard to chat %s", chat_id)
        sent = await client.send_reply_keyboard(
            chat_id=chat_id,
            text="Pick an option:",
            keyboard=[["Yes", "No"], ["Cancel"]],
        )
        logger.info("Reply keyboard sent, message_id=%s", sent.message_id)

        logger.info("Waiting 2 seconds for the keyboard to appear...")
        await asyncio.sleep(2)

        logger.info("Listening for a 'Cancel' message for up to 15 seconds...")
        cancelled = False
        for _ in range(5):
            updates = await client.get_updates(
                chat_id=chat_id, timeout=3, limit=1
            )
            for update in updates:
                text = (
                    update.effective_message.text if update.effective_message else None
                )
                logger.info("Received message: %r", text)
                if text == "Cancel":
                    logger.info("Cancel received, removing the keyboard")
                    await client.remove_reply_keyboard(chat_id=chat_id)
                    cancelled = True
                    break
            if cancelled:
                break
        else:
            logger.info("No 'Cancel' received within 15 seconds")
    finally:
        await client.shutdown()


async def main() -> None:
    if os.environ.get("TELEGRAM_BOT_TOKEN"):
        await _test_real()
    else:
        await _test_mock()
    logger.info("All tests passed")


if __name__ == "__main__":
    asyncio.run(main())
