# Telegram API Microservice

A FastAPI microservice that wraps the Telegram Bot API, exposing HTTP endpoints for sending messages, managing reply keyboards, and fetching updates. The service is packaged as a Docker image for local deployment and includes interactive Swagger UI documentation.

## Getting Started

### Prerequisites

- A Telegram bot token from [@BotFather](https://t.me/BotFather)
- Docker (recommended) **or** Python 3.11+ for local development

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| TELEGRAM_BOT_TOKEN | Yes | — | Your Telegram bot token used to authenticate with the Telegram Bot API |

### Run with Docker (recommended)

1. Build the image:
   ```bash
   docker build -t telegram-api .
   ```

2. Run the container:
   ```bash
   docker compose up --build
   ```

### Run locally (development)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the app:
   ```bash
   TELEGRAM_BOT_TOKEN=your_token uvicorn api.main:app --reload
   ```

### What You Can Do

- Access the interactive Swagger UI at http://localhost:8000/docs to explore and test all endpoints
- Send a health check request: `curl http://localhost:8000/`
- Discover chat IDs from recent updates: `curl "http://localhost:8000/api/v1/get_chat_ids?limit=10"`
- Send messages to Telegram chats via POST /api/v1/send_message
- Send messages with reply keyboards via POST /api/v1/send_reply_keyboard
- Remove reply keyboards via POST /api/v1/remove_reply_keyboard
- Fetch recent updates via POST /api/v1/get_updates
- Run tests without a real token: `python -m pytest tests/test_api.py -v`

## Configuration

All configuration is done through environment variables. See the Environment Variables table above.
