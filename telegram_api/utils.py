"""Small Telegram API wrapper for sending messages and reading updates."""

import logging
import os
from typing import Any, List, Optional

from telegram import (
    Bot,
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramClient:
    """Thin wrapper around python-telegram-bot's Bot class.

    The bot token is read from the ``TELEGRAM_BOT_TOKEN`` environment variable
    unless it is provided explicitly.
    """

    def __init__(
        self, token: Optional[str] = None, offset_path: Optional[str] = None
    ) -> None:
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN")
        if not self.token:
            raise ValueError(
                "A Telegram bot token is required. "
                "Set the TELEGRAM_BOT_TOKEN environment variable or pass it explicitly."
            )
        self.bot = Bot(token=self.token)
        self.offset_path = offset_path
        self._last_update_id: int = self._load_offset() if offset_path else 0

    async def send_message(
        self, chat_id: int, text: str, **kwargs: Any
    ) -> Any:
        """Send ``text`` to ``chat_id``.

        All extra keyword arguments are forwarded to ``Bot.send_message``.
        """
        if not text:
            raise ValueError("Message text cannot be empty.")

        logger.info("Sending message to chat %s", chat_id)
        try:
            return await self.bot.send_message(
                chat_id=chat_id, text=text, **kwargs
            )
        except TelegramError as exc:
            logger.error("Failed to send message to chat %s: %s", chat_id, exc)
            raise

    async def send_reply_keyboard(
        self,
        chat_id: int,
        text: str,
        keyboard: List[List[str]],
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        **kwargs: Any,
    ) -> Any:
        """Send ``text`` to ``chat_id`` with a reply keyboard.

        ``keyboard`` is a list of rows; each row is a list of button labels.

        Example:
            [["Yes", "No"], ["Cancel"]]

        Extra keyword arguments are forwarded to ``send_message``.
        """
        if not text:
            raise ValueError("Message text cannot be empty.")
        if not keyboard:
            raise ValueError("Keyboard cannot be empty.")

        buttons = [
            [KeyboardButton(text=label) for label in row]
            for row in keyboard
        ]
        reply_markup = ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
        )
        return await self.send_message(
            chat_id=chat_id, text=text, reply_markup=reply_markup, **kwargs
        )

    async def remove_reply_keyboard(
        self, chat_id: int, text: str = "Keyboard removed.", **kwargs: Any
    ) -> Any:
        """Send a message that removes the current reply keyboard from the chat.

        All extra keyword arguments are forwarded to ``send_message``.
        """
        if not text:
            raise ValueError("Message text cannot be empty.")

        return await self.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=ReplyKeyboardRemove(),
            **kwargs,
        )

    async def get_updates(
        self,
        chat_id: Optional[int] = None,
        limit: int = 10,
        timeout: int = 0,
    ) -> List[Update]:
        """Fetch recent updates and optionally filter by ``chat_id``.

        The wrapper keeps track of the last processed update ID so that the same
        updates are not returned twice.
        """
        try:
            updates = await self.bot.get_updates(
                offset=self._last_update_id + 1,
                limit=limit,
                timeout=timeout,
            )
        except TelegramError as exc:
            logger.error("Failed to fetch updates: %s", exc)
            raise

        if updates:
            self._last_update_id = max(update.update_id for update in updates)
            self._save_offset()

        if chat_id is not None:
            updates = [
                update
                for update in updates
                if self._match_chat(update, chat_id)
            ]

        return updates

    @staticmethod
    def _match_chat(update: Update, chat_id: Optional[int]) -> bool:
        if chat_id is None:
            return True
        return bool(update.effective_chat and update.effective_chat.id == int(chat_id))

    def _load_offset(self) -> int:
        if not self.offset_path:
            return 0
        try:
            with open(self.offset_path, "r") as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return 0

    def _save_offset(self) -> None:
        if not self.offset_path:
            return
        try:
            with open(self.offset_path, "w") as f:
                f.write(str(self._last_update_id))
        except OSError as exc:
            logger.warning("Could not save update offset: %s", exc)

    async def shutdown(self) -> None:
        """Clean up the underlying bot session."""
        await self.bot.shutdown()
