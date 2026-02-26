"""Shared logging setup: dual console + timestamped file handler.

Usage in any script:

    from log_utils import setup_logging
    log = setup_logging()          # auto-detects script name
    log.info("hello %s", "world")

Log files are written to  log/{script_name}_{YYYYMMDD_HHMMSS}.log
Both handlers flush immediately (no buffering).
"""

import logging
import os
import sys
from datetime import datetime

LOG_DIR = "log"


def setup_logging(script_name: str | None = None, level: int = logging.INFO) -> logging.Logger:
    """Configure and return a logger that writes to both stderr and a log file.

    Args:
        script_name: Base name used for the log file. Defaults to the
                     calling script's filename without extension.
        level:       Logging level (default INFO).
    """
    if script_name is None:
        script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]

    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"{script_name}_{timestamp}.log")

    fmt = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(level)
    file_handler.setFormatter(fmt)

    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setLevel(level)
    console_handler.setFormatter(fmt)

    logger = logging.getLogger(script_name)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.info("Logging to %s", log_path)
    return logger
