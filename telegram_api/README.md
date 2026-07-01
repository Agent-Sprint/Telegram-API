# Telegram API utils

A small Python wrapper around the Telegram Bot API using
[`python-telegram-bot`](https://github.com/python-telegram-bot/python-telegram-bot).

## Features

- `send_message(chat_id, text)` – send a message to a chat.
- `send_reply_keyboard(chat_id, text, keyboard)` – send a message with a reply keyboard.
- `remove_reply_keyboard(chat_id)` – remove the current reply keyboard from the chat.
- `get_updates(chat_id=None)` – fetch recent updates and optionally filter by chat.

## 1. Create a Telegram bot

1. Open Telegram and search for **@BotFather**.
2. Send `/newbot`.
3. Pick a display name and a username ending in `bot` (e.g. `mydevinbot`).
4. Copy the **HTTP API token** you receive.
5. Open your new bot in Telegram and press **Start**.

## 2. Install the dependency

From the `Devin-Docker` folder (where `requirements.txt` lives):

```bash
pip install -r requirements.txt
```

Or directly:

```bash
pip install python-telegram-bot==22.8
```

## 3. Set your token and chat ID

Export the token and the chat ID you want to test with.

```bash
# Linux / macOS / WSL
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="123456789"
```

```powershell
# Windows PowerShell
$env:TELEGRAM_BOT_TOKEN = "your_bot_token"
$env:TELEGRAM_CHAT_ID = "123456789"
```

To get your `chat_id`:

**Option 1 — helper script (easiest):**

Run this from the `Devin-Docker` folder after setting your token:

```bash
python -m telegram_api.get_ids
```

It will print the chat IDs from the latest updates. If nothing appears, send a message to the bot first.

**Option 2 — browser:**

1. Send a message to your bot.
2. Open `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates` in a browser.
3. Look at the JSON: `message.chat.id` is the chat ID.

## 4. Test the API end-to-end

Run the test from the `Devin-Docker` folder:

```bash
python -m telegram_api.test
```

It will:

1. Send a test message to `TELEGRAM_CHAT_ID`.
2. Fetch updates for `TELEGRAM_CHAT_ID`.
3. Print the sent message ID and the received update IDs.

If `TELEGRAM_BOT_TOKEN` is missing, it runs a mock smoke test instead.

The test script stores a `.telegram_offset` file in the current directory so the
same updates are not returned on the next run. Delete the file to re-fetch all
updates.

## Use in your own code

```python
import asyncio
from telegram_api import TelegramClient

async def main():
    client = TelegramClient()
    await client.send_message(
        chat_id=123456789, text="Hello!"
    )
    updates = await client.get_updates(chat_id=123456789)
    print(updates)
    await client.shutdown()

asyncio.run(main())
```

Send a reply keyboard:

```python
await client.send_reply_keyboard(
    chat_id=123456789,
    text="Choose an option:",
    keyboard=[["Yes", "No"], ["Cancel"]],
)
```

Remove the keyboard later:

```python
await client.remove_reply_keyboard(chat_id=123456789)
```
