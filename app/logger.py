"""
Logging configuration for the application.
"""

import logging
import os
import sys
from typing import Optional


def setup_logger(name: Optional[str] = None, level: Optional[int] = None) -> logging.Logger:
    """
    Set up and configure a logger with console handler.

    Args:
        name: Logger name (defaults to 'app')
        level: Log level (defaults to INFO or from LOG_LEVEL env var)

    Returns:
        Configured logger instance
    """
    # Get log level from environment or use INFO
    if level is None:
        log_level_str = os.environ.get("LOG_LEVEL", "INFO").upper()
        level = getattr(logging, log_level_str, logging.INFO)

    tmp_logger = logging.getLogger(name or "app")

    # Don't add handlers if they already exist (prevents duplicate logs)
    if tmp_logger.handlers:
        tmp_logger.setLevel(level)
        return tmp_logger

    # Set log level
    tmp_logger.setLevel(level)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Create formatter with detailed information
    formatter = logging.Formatter(fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    console_handler.setFormatter(formatter)

    # Add handler to tmp_logger
    tmp_logger.addHandler(console_handler)

    # Prevent propagation to root tmp_logger to avoid duplicate logs
    tmp_logger.propagate = False

    return tmp_logger


# Create the main application logger
logger = setup_logger("app")
