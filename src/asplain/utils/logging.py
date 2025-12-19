"""
Setup project wide loggers.

This is a thin wrapper around Python's logging module. It supports colored
logging.
"""

import logging
import os
from typing import TextIO

NOTSET = logging.NOTSET
DEBUG = logging.DEBUG
INFO = logging.INFO
WARNING = logging.WARNING
ERROR = logging.ERROR
CRITICAL = logging.CRITICAL

COLORS = {
    "GREY": "\033[90m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
    "NORMAL": "\033[0m",
}
log = logging.getLogger(__name__)


def colored(color: str, s: str) -> str:
    """
    Returns the string colored by the given color.

    Args:
        color (str): A color name: GREY, BLUE, GREEN, YELLOW, RED
    """
    return f"{COLORS[color.upper()]}{s}{COLORS['NORMAL']}"


class SingleLevelFilter(logging.Filter):
    """
    Filter levels.
    """

    passlevel: int
    reject: bool

    def __init__(self, passlevel: int, reject: bool):
        # pylint: disable=super-init-not-called
        self.passlevel = passlevel
        self.reject = reject

    def filter(self, record: logging.LogRecord) -> bool:
        if self.reject:
            return record.levelno != self.passlevel  # nocoverage

        return record.levelno == self.passlevel


_current_logging_level = None  # Module-level variable to store the configured level


def configure_logging(stream: TextIO, level: int, use_color: bool) -> None:
    """
    Configure application logging.
    """
    global _current_logging_level
    _current_logging_level = level

    def format_str(color: str) -> str:
        if use_color:
            return f"{COLORS[color]}%(levelname)s:{COLORS['GREY']}  - %(message)s{COLORS['NORMAL']}"
        return "%(levelname)s:  - %(message)s"  # nocoverage

    def make_handler(level: int, color: str) -> "logging.StreamHandler[TextIO]":
        handler = logging.StreamHandler(stream)
        handler.addFilter(SingleLevelFilter(level, False))
        handler.setLevel(level)
        formatter = logging.Formatter(format_str(color))
        handler.setFormatter(formatter)
        return handler

    handlers = [
        make_handler(logging.INFO, "GREEN"),
        make_handler(logging.WARNING, "YELLOW"),
        make_handler(logging.DEBUG, "BLUE"),
        make_handler(logging.ERROR, "RED"),
    ]

    # 1️⃣ Root logger: quiet, no handlers
    root = logging.getLogger()
    root.handlers.clear()
    root.setLevel(logging.WARNING)

    # 2️⃣ Project logger: owns handlers
    project_logger = logging.getLogger("asplain")
    project_logger.handlers.clear()
    project_logger.setLevel(level)
    project_logger.propagate = False

    for h in handlers:
        project_logger.addHandler(h)


def get_configured_logging_level() -> int | None:
    """
    Returns the logging level that was last set by configure_logging.
    """
    return _current_logging_level


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the given name.
    """
    return logging.getLogger(name)


def save_out(file_name: str, content: str) -> None:
    """
    Save content to a file if the logging level is low enough.

    Args:
        file_path: The path to the file.
        content: The content to save.
    """
    if _current_logging_level is DEBUG or _current_logging_level is INFO:  # 30 is WARNING, 40 is ERROR
        return
    out_dir = os.path.join(os.getcwd(), "out")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, file_name)
    with open(out_path, "w") as f:
        f.write(content)
    log.info("Saved output to %s", out_path)
