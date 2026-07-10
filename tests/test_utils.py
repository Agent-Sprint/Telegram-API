"""Unit tests for telegram_api.utils — Whisper singleton pattern.

The module loads the Whisper model once at import time. These tests verify:
- load_model is called exactly once (not per transcription call)
- device is hardcoded to "cpu"
- the WHISPER_MODEL env var controls which model is loaded
- transcribe_voice returns the stripped transcript on success
- transcribe_voice returns "transcription failed" on exception

whisper is NOT installed in the local dev environment (it lives in Docker),
so sys.modules is patched with a MagicMock stub before each import.
"""

import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_whisper_stub() -> MagicMock:
    """Return (and register if needed) a fresh MagicMock for the whisper module."""
    stub = MagicMock()
    sys.modules["whisper"] = stub
    return stub


def _reload_utils(whisper_stub: MagicMock) -> object:
    """Remove telegram_api.utils from sys.modules and re-import it so the
    module-level singleton code runs against the provided stub."""
    for key in list(sys.modules):
        if key in ("telegram_api.utils", "telegram_api"):
            del sys.modules[key]
    import telegram_api.utils  # noqa: F401 — side-effect import
    return telegram_api.utils


def _fake_voice(file_id: str = "test_file_id") -> MagicMock:
    voice = MagicMock()
    voice.file_id = file_id
    return voice


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_whisper_model_loaded_at_module_level():
    """whisper.load_model is called exactly once on module import."""
    stub = _get_whisper_stub()
    mock_model = MagicMock()
    stub.load_model = MagicMock(return_value=mock_model)

    _reload_utils(stub)

    assert stub.load_model.call_count == 1, (
        f"Expected load_model to be called once, got {stub.load_model.call_count}"
    )


def test_transcribe_voice_uses_cpu():
    """whisper.load_model is always called with device='cpu'."""
    stub = _get_whisper_stub()
    stub.load_model = MagicMock(return_value=MagicMock())

    _reload_utils(stub)

    stub.load_model.assert_called_once()
    kwargs = stub.load_model.call_args.kwargs
    assert kwargs.get("device") == "cpu", (
        f"Expected device='cpu', got {kwargs.get('device')!r}"
    )


def test_transcribe_voice_uses_env_model_name():
    """WHISPER_MODEL env var determines the model name passed to load_model."""
    stub = _get_whisper_stub()
    stub.load_model = MagicMock(return_value=MagicMock())

    with patch.dict(os.environ, {"WHISPER_MODEL": "tiny"}, clear=False):
        _reload_utils(stub)

    stub.load_model.assert_called_once()
    args = stub.load_model.call_args.args
    assert args[0] == "tiny", f"Expected model name 'tiny', got {args[0]!r}"


def test_transcribe_voice_returns_text():
    """transcribe_voice returns stripped text on success."""
    stub = _get_whisper_stub()
    mock_model = MagicMock()
    mock_model.transcribe = MagicMock(return_value={"text": "  hello world  "})
    stub.load_model = MagicMock(return_value=mock_model)

    utils = _reload_utils(stub)

    async def _run():
        voice = _fake_voice("voice_123")
        bot = AsyncMock()
        tg_file = AsyncMock()
        tg_file.download_to_drive = AsyncMock()
        bot.get_file = AsyncMock(return_value=tg_file)

        with patch("telegram_api.utils.os.path.exists", return_value=True), \
             patch("telegram_api.utils.os.remove"):
            return await utils.transcribe_voice(voice, bot)

    result = asyncio.run(_run())
    assert result == "hello world"
    # load_model must NOT have been called again (singleton)
    assert stub.load_model.call_count == 1


def test_transcribe_voice_returns_failure_on_exception():
    """transcribe_voice returns 'transcription failed' when transcription raises."""
    stub = _get_whisper_stub()
    mock_model = MagicMock()
    mock_model.transcribe = MagicMock(side_effect=Exception("boom"))
    stub.load_model = MagicMock(return_value=mock_model)

    utils = _reload_utils(stub)

    async def _run():
        voice = _fake_voice("voice_456")
        bot = AsyncMock()
        tg_file = AsyncMock()
        tg_file.download_to_drive = AsyncMock()
        bot.get_file = AsyncMock(return_value=tg_file)

        with patch("telegram_api.utils.os.path.exists", return_value=True), \
             patch("telegram_api.utils.os.remove") as mock_remove:
            result = await utils.transcribe_voice(voice, bot)
            mock_remove.assert_called_once()
            return result

    assert asyncio.run(_run()) == "transcription failed"
