# Telegram API Microservice

FastAPI HTTP wrapper around the Telegram Bot API. The service exposes every `TelegramClient` method as a REST endpoint.

## Endpoints

Base path: `/api/v1`

Interactive Swagger UI: `http://localhost:8000/docs`

### Health check

- `GET /`
- Response: `{"status": "ok", "service": "telegram-api"}`

### Get chat IDs

Use this after sending a message to your bot to discover the `chat_id` you need for the other endpoints.

- `GET /api/v1/get_chat_ids?limit=10`
- Response:
  ```json
  {
    "success": true,
    "chat_ids": [
      {"chat_id": 123456789, "text": "Hi bot"}
    ],
    "error": null
  }
  ```

### Send a message

- `POST /api/v1/send_message`
- Body:
  ```json
  {
    "chat_id": 123456789,
    "text": "Hello from the bot!"
  }
  ```
- Response:
  ```json
  {
    "success": true,
    "message_id": 42,
    "error": null
  }
  ```

### Send a reply keyboard

- `POST /api/v1/send_reply_keyboard`
- Body:
  ```json
  {
    "chat_id": 123456789,
    "text": "Pick an option",
    "keyboard": [["Yes", "No"], ["Cancel"]],
    "resize_keyboard": true,
    "one_time_keyboard": false
  }
  ```
- Response:
  ```json
  {
    "success": true,
    "message_id": 42,
    "error": null
  }
  ```

### Remove a reply keyboard

- `POST /api/v1/remove_reply_keyboard`
- Body:
  ```json
  {
    "chat_id": 123456789,
    "text": "Keyboard removed."
  }
  ```
- Response:
  ```json
  {
    "success": true,
    "message_id": 42,
    "error": null
  }
  ```

### Get updates

- `POST /api/v1/get_updates`
- Body:
  ```json
  {
    "chat_id": 123456789,
    "limit": 10,
    "timeout": 0
  }
  ```
- Response:
  ```json
  {
    "success": true,
    "updates": [
      {"update_id": 1, "chat_id": 123456789, "text": "Hello"}
    ],
    "error": null
  }
  ```

## Error responses

- `400` — Validation error (e.g., empty text, empty keyboard, missing `chat_id`).
- `500` — Telegram API error.

## Example usage with curl

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"

# 1. Health check
curl "http://localhost:8000/"

# 2. Send a message to your bot first, then get your chat ID
curl "http://localhost:8000/api/v1/get_chat_ids?limit=10"

# 3. Send a message
curl -X POST "http://localhost:8000/api/v1/send_message" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": 123456789, "text": "Hello!"}'

# 4. Send a reply keyboard
curl -X POST "http://localhost:8000/api/v1/send_reply_keyboard" \
  -H "Content-Type: application/json" \
  -d '{
    "chat_id": 123456789,
    "text": "Pick an option",
    "keyboard": [["Yes", "No"], ["Cancel"]]
  }'

# 5. Remove a reply keyboard
curl -X POST "http://localhost:8000/api/v1/remove_reply_keyboard" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": 123456789, "text": "Keyboard removed."}'

# 6. Get updates
curl -X POST "http://localhost:8000/api/v1/get_updates" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": 123456789, "limit": 10, "timeout": 0}'
```
