"""
Logging utilities for FastAPI application.

This module provides enhanced logging capabilities including:
- JSON formatting for structured logs
- Sensitive data sanitization
- Rotating file handlers with proper configuration
"""

import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from config import settings


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.

    Formats log records as JSON for better parsing and analysis.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sensitive_patterns = [
            re.compile(r'api[_-]?key["\']?\s*[:=]\s*["\']?([^"\'\\s]+)', re.IGNORECASE),
            re.compile(r'password["\']?\s*[:=]\s*["\']?([^"\'\\s]+)', re.IGNORECASE),
            re.compile(r'token["\']?\s*[:=]\s*["\']?([^"\'\\s]+)', re.IGNORECASE),
            re.compile(r'secret["\']?\s*[:=]\s*["\']?([^"\'\\s]+)', re.IGNORECASE),
        ]

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.

        Args:
            record: Log record to format

        Returns:
            JSON-formatted log string
        """
        log_data: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": self._sanitize_message(record.getMessage()),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields from record
        if hasattr(record, "__dict__"):
            for key, value in record.__dict__.items():
                if key not in {
                    "name",
                    "msg",
                    "args",
                    "levelname",
                    "levelno",
                    "pathname",
                    "filename",
                    "module",
                    "exc_info",
                    "exc_text",
                    "stack_info",
                    "lineno",
                    "funcName",
                    "created",
                    "msecs",
                    "relativeCreated",
                    "thread",
                    "threadName",
                    "processName",
                    "process",
                    "getMessage",
                }:
                    log_data[key] = value

        # Add exception information if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, default=str, ensure_ascii=False)

    def _sanitize_message(self, message: str) -> str:
        """
        Sanitize log message to remove sensitive data.

        Args:
            message: Original log message

        Returns:
            Sanitized log message
        """
        sanitized = message
        for pattern in self.sensitive_patterns:
            sanitized = pattern.sub(
                lambda m: f"{m.group(0).split('=')[0]}=***REDACTED***", sanitized
            )
        return sanitized


class ConsoleFormatter(logging.Formatter):
    """
    FastAPI-style console formatter with colors and clean formatting.
    """

    # ANSI color codes (FastAPI-inspired)
    COLORS = {
        "DEBUG": "\033[36m",  # Cyan
        "INFO": "\033[32m",  # Green
        "WARNING": "\033[33m",  # Yellow
        "ERROR": "\033[31m",  # Red
        "CRITICAL": "\033[35m\033[1m",  # Magenta + Bold
    }

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    def __init__(self):
        super().__init__(
            fmt="%(message)s",  # We'll handle formatting in the format method
            datefmt="%H:%M:%S",
        )
        # Check if we should use colors
        self.use_colors = self._supports_color()

    def _supports_color(self) -> bool:
        """
        Check if the terminal supports color output.
        """
        # Check if we're in a terminal
        if not hasattr(sys.stdout, "isatty") or not sys.stdout.isatty():
            return False

        # Check for common environment variables that indicate color support
        term = os.environ.get("TERM", "").lower()
        if "color" in term or term in ("xterm", "xterm-256color", "screen", "linux"):
            return True

        # Check for Windows Terminal or other modern terminals
        if os.environ.get("WT_SESSION") or os.environ.get("COLORTERM"):
            return True

        # Default to True for Unix-like systems
        return os.name != "nt"

    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record with FastAPI-style colors and layout.
        """
        # Get level info
        level = record.levelname

        # Get the message
        message = record.getMessage()

        if self.use_colors:
            # FastAPI-style colored format
            level_color = self.COLORS.get(level, "")
            formatted = f"     {level_color}{level:<8}{self.RESET} {message}"
        else:
            # Plain format (no colors)
            formatted = f"     {level:<8} {message}"

        # Add exception info if present
        if record.exc_info:
            formatted += "\n" + self.formatException(record.exc_info)

        return formatted


def setup_logging() -> None:
    """
    Set up comprehensive logging configuration.

    Configures both console and file logging with appropriate formatters.
    """
    # Create logs directory if it doesn't exist
    if settings.LOG_TO_FILE:
        log_dir = Path(settings.LOG_FILE_PATH)
        log_dir.mkdir(exist_ok=True)

    # Root logger configuration
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

    # Remove existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handlers = []

    # Console handler (always enabled for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))
    console_handler.setFormatter(ConsoleFormatter())
    handlers.append(console_handler)

    # File handler (configurable)
    if settings.LOG_TO_FILE:
        log_file_path = Path(settings.LOG_FILE_PATH) / settings.LOG_FILE_NAME

        file_handler = RotatingFileHandler(
            filename=log_file_path,
            maxBytes=settings.LOG_MAX_BYTES,
            backupCount=settings.LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
        file_handler.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

        if settings.LOG_JSON_FORMAT:
            file_handler.setFormatter(JSONFormatter())
        else:
            file_handler.setFormatter(ConsoleFormatter())

        handlers.append(file_handler)

    # Add all handlers to root logger
    for handler in handlers:
        root_logger.addHandler(handler)

    # Log configuration startup
    logger = logging.getLogger(__name__)
    logger.info(
        "Logging configuration initialized",
        extra={
            "log_level": settings.LOG_LEVEL,
            "log_to_file": settings.LOG_TO_FILE,
            "log_file_path": str(Path(settings.LOG_FILE_PATH) / settings.LOG_FILE_NAME)
            if settings.LOG_TO_FILE
            else None,
            "json_format": settings.LOG_JSON_FORMAT,
            "max_file_size_mb": settings.LOG_MAX_BYTES / 1024 / 1024,
            "backup_count": settings.LOG_BACKUP_COUNT,
        },
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with consistent configuration.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
