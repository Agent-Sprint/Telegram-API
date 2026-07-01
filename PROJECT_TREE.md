# Project Tree

## Telegram-API

api/
├── __init__.py [x]
├── main.py [x]
│   ├── function startup_event() [x]
│   │   ├── Functionality:
│   │   │   - Initialize global TelegramClient instance from TELEGRAM_BOT_TOKEN env var
│   │   │   - Handle missing token gracefully
│   │   ├── Input:
│   │   │   - None (reads from environment)
│   │   └── Output:
│   │       - None
│   │       - Raises ValueError if token is missing
│   ├── function shutdown_event() [x]
│   │   ├── Functionality:
│   │   │   - Call client.shutdown() to clean up bot session
│   │   ├── Input:
│   │   │   - None
│   │   └── Output:
│   │       - None
│   ├── function health_check() [x]
│   │   ├── Functionality:
│   │   │   - Return service status for health check
│   │   ├── Input:
│   │   │   - None
│   │   └── Output:
│   │       - dict with status information
│   ├── function send_message() [x]
│   │   ├── Functionality:
│   │   │   - Accept SendMessageRequest and call TelegramClient.send_message
│   │   │   - Wrap in try/except for error handling
│   │   │   - Return appropriate success/error responses
│   │   ├── Input:
│   │   │   - request: SendMessageRequest
│   │   └── Output:
│   │       - MessageResponse
│   ├── function send_reply_keyboard() [x]
│   │   ├── Functionality:
│   │   │   - Accept SendReplyKeyboardRequest and call TelegramClient.send_reply_keyboard
│   │   │   - Wrap in try/except for error handling
│   │   │   - Return appropriate success/error responses
│   │   ├── Input:
│   │   │   - request: SendReplyKeyboardRequest
│   │   └── Output:
│   │       - MessageResponse
│   ├── function remove_reply_keyboard() [x]
│   │   ├── Functionality:
│   │   │   - Accept RemoveReplyKeyboardRequest and call TelegramClient.remove_reply_keyboard
│   │   │   - Wrap in try/except for error handling
│   │   │   - Return appropriate success/error responses
│   │   ├── Input:
│   │   │   - request: RemoveReplyKeyboardRequest
│   │   └── Output:
│   │       - MessageResponse
│   ├── function get_chat_ids() [x]
│   │   ├── Functionality:
│   │   │   - Accept GetChatIdsRequest and return unique chat IDs from recent updates
│   │   │   - Call TelegramClient.get_updates and extract chat IDs
│   │   │   - Wrap in try/except for error handling
│   │   ├── Input:
│   │   │   - request: GetChatIdsRequest
│   │   └── Output:
│   │       - ChatIdsResponse
│   └── function get_updates() [x]
│       ├── Functionality:
│       │   - Accept GetUpdatesRequest and call TelegramClient.get_updates
│       │   - Wrap in try/except for error handling
│       │   - Return appropriate success/error responses
│       ├── Input:
│       │   - request: GetUpdatesRequest
│       └── Output:
│           - UpdatesResponse
├── models.py [x]
│   ├── class SendMessageRequest [x]
│   │   ├── Functionality:
│   │   │   - Pydantic model for send_message endpoint
│   │   │   - Include json_schema_extra examples for Swagger UI
│   │   ├── Input:
│   │   │   - chat_id: int
│   │   │   - text: str
│   │   │   - kwargs: Optional[Dict[str, Any]]
│   │   └── Output:
│   │       - Validated Pydantic model instance
│   ├── class SendReplyKeyboardRequest [x]
│   │   ├── Functionality:
│   │   │   - Pydantic model for send_reply_keyboard endpoint
│   │   │   - Include json_schema_extra examples for Swagger UI
│   │   ├── Input:
│   │   │   - chat_id: int
│   │   │   - text: str
│   │   │   - keyboard: List[List[str]]
│   │   │   - resize_keyboard: bool = True
│   │   │   - one_time_keyboard: bool = False
│   │   │   - kwargs: Optional[Dict[str, Any]]
│   │   └── Output:
│   │       - Validated Pydantic model instance
│   ├── class RemoveReplyKeyboardRequest [x]
│   │   ├── Functionality:
│   │   │   - Pydantic model for remove_reply_keyboard endpoint
│   │   │   - Include json_schema_extra examples for Swagger UI
│   │   ├── Input:
│   │   │   - chat_id: int
│   │   │   - text: str = "Keyboard removed."
│   │   │   - kwargs: Optional[Dict[str, Any]]
│   │   └── Output:
│   │       - Validated Pydantic model instance
│   ├── class GetUpdatesRequest [x]
│   │   ├── Functionality:
│   │   │   - Pydantic model for get_updates endpoint
│   │   │   - Include json_schema_extra examples for Swagger UI
│   │   ├── Input:
│   │   │   - chat_id: Optional[int] = None
│   │   │   - limit: int = 10
│   │   │   - timeout: int = 0
│   │   └── Output:
│   │       - Validated Pydantic model instance
│   ├── class GetChatIdsRequest [x]
│   │   ├── Functionality:
│   │   │   - Pydantic model for get_chat_ids endpoint
│   │   │   - Include json_schema_extra examples for Swagger UI
│   │   ├── Input:
│   │   │   - limit: int = 10
│   │   └── Output:
│   │       - Validated Pydantic model instance
│   ├── class MessageResponse [x]
│   │   ├── Functionality:
│   │   │   - Pydantic model for message operation responses
│   │   ├── Input:
│   │   │   - success: bool
│   │   │   - message_id: Optional[int] = None
│   │   │   - error: Optional[str] = None
│   │   └── Output:
│   │       - Validated Pydantic model instance
│   ├── class UpdatesResponse [x]
│   │   ├── Functionality:
│   │   │   - Pydantic model for get_updates responses
│   │   ├── Input:
│   │   │   - success: bool
│   │   │   - updates: List[Dict[str, Any]]
│   │   │   - error: Optional[str] = None
│   │   └── Output:
│   │       - Validated Pydantic model instance
│   └── class ChatIdsResponse [x]
│       ├── Functionality:
│       │   - Pydantic model for get_chat_ids responses
│       ├── Input:
│       │   - success: bool
│       │   - chat_ids: List[Dict[str, Any]]
│       │   - error: Optional[str] = None
│       └── Output:
│           - Validated Pydantic model instance
├── router.py [x]
│   ├── function create_router() [x]
│   │   ├── Functionality:
│   │   │   - Create APIRouter with prefix /api/v1
│   │   │   - Organize all endpoints into the router
│   │   │   - Allow future versioning
│   │   ├── Input:
│   │   │   - None
│   │   └── Output:
│   │       - APIRouter instance
│   └── function include_router() [x]
│       ├── Functionality:
│       │   - Include router in main FastAPI app
│       ├── Input:
│       │   - app: FastAPI
│       │   - router: APIRouter
│       └── Output:
│           - None
└── README.md [x]
    ├── Functionality:
    │   - Document API endpoint reference
    │   - Document request/response schema
    │   - Provide concrete example requests for every route
    │   - Provide usage examples with curl or Python requests
    ├── Input:
    │   - None
    └── Output:
        - Markdown documentation file
telegram_api/
├── __init__.py [x]
│   └── Functionality:
│       - Export TelegramClient from utils
│       - Define __all__ for package exports
├── utils.py [x]
│   └── class TelegramClient
│       ├── method __init__() [x]
│       │   ├── Functionality:
│       │   │   - Initialize TelegramClient with token from env or parameter
│       │   │   - Initialize Bot instance
│       │   │   - Load offset from file if offset_path provided
│       │   ├── Input:
│       │   │   - token: Optional[str]
│       │   │   - offset_path: Optional[str]
│       │   └── Output:
│       │       - None
│       │       - Raises ValueError if token is missing
│       ├── method send_message() [x]
│       │   ├── Functionality:
│       │   │   - Send text message to chat_id
│       │   │   - Forward extra kwargs to Bot.send_message
│       │   │   - Validate text is not empty
│       │   ├── Input:
│       │   │   - chat_id: int
│       │   │   - text: str
│       │   │   - **kwargs: Any
│       │   └── Output:
│       │       - Message object from Telegram API
│       │       - Raises ValueError if text is empty
│       │       - Raises TelegramError on API failure
│       ├── method send_reply_keyboard() [x]
│       │   ├── Functionality:
│       │   │   - Send message with reply keyboard
│       │   │   - Convert keyboard list to ReplyKeyboardMarkup
│       │   │   - Validate text and keyboard are not empty
│       │   ├── Input:
│       │   │   - chat_id: int
│       │   │   - text: str
│       │   │   - keyboard: List[List[str]]
│       │   │   - resize_keyboard: bool = True
│       │   │   - one_time_keyboard: bool = False
│       │   │   - **kwargs: Any
│       │   └── Output:
│       │       - Message object from Telegram API
│       │       - Raises ValueError if text or keyboard is empty
│       ├── method remove_reply_keyboard() [x]
│       │   ├── Functionality:
│       │   │   - Send message that removes reply keyboard
│       │   │   - Use ReplyKeyboardRemove markup
│       │   │   - Validate text is not empty
│       │   ├── Input:
│       │   │   - chat_id: int
│       │   │   - text: str = "Keyboard removed."
│       │   │   - **kwargs: Any
│       │   └── Output:
│       │       - Message object from Telegram API
│       │       - Raises ValueError if text is empty
│       ├── method get_updates() [x]
│       │   ├── Functionality:
│       │   │   - Fetch recent updates from Telegram
│       │   │   - Track last update ID to avoid duplicates
│       │   │   - Optionally filter by chat_id
│       │   │   - Save offset to file if offset_path provided
│       │   ├── Input:
│       │   │   - chat_id: Optional[int] = None
│       │   │   - limit: int = 10
│       │   │   - timeout: int = 0
│       │   └── Output:
│       │       - List[Update] from Telegram API
│       │       - Raises TelegramError on API failure
│       ├── method _match_chat() [x]
│       │   ├── Functionality:
│       │   │   - Static method to check if update matches chat_id
│       │   ├── Input:
│       │   │   - update: Update
│       │   │   - chat_id: Optional[int]
│       │   └── Output:
│       │       - bool
│       ├── method _load_offset() [x]
│       │   ├── Functionality:
│       │   │   - Load last update ID from offset file
│       │   ├── Input:
│       │   │   - None
│       │   └── Output:
│       │       - int (offset value, 0 if file missing or invalid)
│       ├── method _save_offset() [x]
│       │   ├── Functionality:
│       │   │   - Save last update ID to offset file
│       │   ├── Input:
│       │   │   - None
│       │   └── Output:
│       │       - None
│       │       - Logs warning if save fails
│       └── method shutdown() [x]
│           ├── Functionality:
│           │   - Clean up underlying bot session
│           ├── Input:
│           │   - None
│           └── Output:
│               - None
├── test.py [x]
│   └── function main()
│       ├── Functionality:
│       │   - Run mock smoke test if TELEGRAM_BOT_TOKEN not set
│       │   - Run real integration test if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID set
│       ├── Input:
│       │   - None (uses environment variables)
│       └── Output:
│           - None
│           - Prints test results to stdout
├── get_ids.py [x]
│   └── function main()
│       ├── Functionality:
│       │   - Fetch latest Telegram updates
│       │   - Print chat IDs and message text
│       │   - Help users discover their chat ID
│       ├── Input:
│       │   - None (uses TELEGRAM_BOT_TOKEN env var)
│       └── Output:
│           - None
│           - Prints chat IDs to stdout
└── README.md [x]
    ├── Functionality:
    │   - Document usage of TelegramClient
    │   - Provide examples for all methods
    ├── Input:
    │   - None
    └── Output:
        - Markdown documentation file
tests/
├── __init__.py [ ]
└── test_api.py [ ]
    ├── function test_health_check() [ ]
    │   ├── Functionality:
    │   │   - Test health check endpoint returns 200
    │   │   - Mock TelegramClient
    │   ├── Input:
    │   │   - None
    │   └── Output:
    │       - None (assertion-based test)
    ├── function test_send_message() [ ]
    │   ├── Functionality:
    │   │   - Test send_message endpoint with valid payload
    │   │   - Test with invalid payload (empty text)
    │   │   - Mock TelegramClient.send_message
    │   ├── Input:
    │   │   - None
    │   └── Output:
    │       - None (assertion-based test)
    ├── function test_send_reply_keyboard() [ ]
    │   ├── Functionality:
    │   │   - Test send_reply_keyboard endpoint with valid payload
    │   │   - Test with invalid payload (empty keyboard)
    │   │   - Mock TelegramClient.send_reply_keyboard
    │   ├── Input:
    │   │   - None
    │   └── Output:
    │       - None (assertion-based test)
    ├── function test_remove_reply_keyboard() [ ]
    │   ├── Functionality:
    │   │   - Test remove_reply_keyboard endpoint with valid payload
    │   │   - Mock TelegramClient.remove_reply_keyboard
    │   ├── Input:
    │   │   - None
    │   └── Output:
    │       - None (assertion-based test)
    ├── function test_get_updates() [ ]
    │   ├── Functionality:
    │   │   - Test get_updates endpoint with valid payload
    │   │   - Mock TelegramClient.get_updates
    │   ├── Input:
    │   │   - None
    │   └── Output:
    │       - None (assertion-based test)
    ├── function test_get_chat_ids() [ ]
    │   ├── Functionality:
    │   │   - Test get_chat_ids endpoint with valid payload
    │   │   - Mock TelegramClient.get_updates
    │   ├── Input:
    │   │   - None
    │   └── Output:
    │       - None (assertion-based test)
    └── function test_error_handling() [ ]
        ├── Functionality:
        │   - Test error handling for TelegramError exceptions
        │   - Mock TelegramClient to raise TelegramError
        ├── Input:
        │   - None
        └── Output:
            - None (assertion-based test)
.dockerignore [x]
Dockerfile [x]
docker-compose.yml [x]
README.md [x]
├── Functionality:
│   - Update with FastAPI and Docker instructions
│   - Add local run instructions with uvicorn
│   - Add Docker build and run instructions
│   - Add API endpoint documentation with examples
│   - Add environment variable requirements
├── Input:
│   - None
└── Output:
    - Updated Markdown documentation file
requirements.txt [x]
