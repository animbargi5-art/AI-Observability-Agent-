"""
===============================================================================
TattvaAI - Central Logging Configuration
===============================================================================

This module provides centralized logging configuration for the entire
TattvaAI Autonomous Incident Investigation Platform.

Goals:
    • Consistent logging across all modules
    • Console and file logging
    • Easy debugging
    • Production-ready logging
    • Future integration with SigNoz/OpenTelemetry

===============================================================================
"""

import logging
import logging.config
from pathlib import Path


# =============================================================================
# Log Directory
# =============================================================================

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)


# =============================================================================
# Logging Configuration
# =============================================================================

LOGGING_CONFIG = {
    "version": 1,

    "disable_existing_loggers": False,

    "formatters": {

        "default": {

            "format": (
                "%(asctime)s | "
                "%(levelname)-8s | "
                "%(name)s | "
                "%(message)s"
            )

        },

        "detailed": {

            "format": (
                "%(asctime)s | "
                "%(levelname)-8s | "
                "%(name)s | "
                "%(filename)s:%(lineno)d | "
                "%(message)s"
            )

        }

    },

    "handlers": {

        "console": {

            "class": "logging.StreamHandler",

            "formatter": "default",

            "level": "INFO"

        },

        "file": {

            "class": "logging.FileHandler",

            "filename": LOG_DIR / "tattva_ai.log",

            "formatter": "detailed",

            "level": "DEBUG",

            "encoding": "utf-8"

        }

    },

    "root": {

        "handlers": ["console", "file"],

        "level": "INFO"

    }

}


# =============================================================================
# Configure Logging
# =============================================================================

def configure_logging() -> None:
    """
    Configure application-wide logging.

    Call this once during FastAPI startup.
    """

    logging.config.dictConfig(LOGGING_CONFIG)


# =============================================================================
# Get Logger
# =============================================================================

def get_logger(name: str) -> logging.Logger:
    """
    Return a named logger.
    """
    return logging.getLogger(name)


# Configure logging once when this module is imported
configure_logging()

# Global logger used throughout the application
logger = get_logger("TattvaAI")