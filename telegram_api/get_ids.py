"""Fetch the latest Telegram updates and print the chat ID.

Set TELEGRAM_BOT_TOKEN, then run this script. It will query the Telegram API and
print the chat_id from each update so you can copy it into your environment
variables.
"""

import asyncio
import os

from telegram_api import TelegramClient


async def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Set TELEGRAM_BOT_TOKEN environment variable first.")
        return

    client = TelegramClient(token=token)
    try:
        print("Fetching updates from Telegram...")
        updates = await client.get_updates(limit=10)
        if not updates:
            print("No updates found. Send a message to the bot first.")
            return

        seen = set()
        for update in updates:
            chat_id = update.effective_chat.id if update.effective_chat else None
            text = update.message.text if update.message else None
            if chat_id not in seen:
                seen.add(chat_id)
                print(f"chat_id: {chat_id}, text: {text!r}")
    finally:
        await client.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
