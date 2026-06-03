"""
Logger configuration for UK Sky Carrier Lookup System
"""

import logging
import logging.handlers
from datetime import datetime
import config

# Create logger
logger = logging.getLogger("SKY_LOOKUP")
logger.setLevel(getattr(logging, config.LOG_LEVEL))

# Create logs directory if it doesn't exist
import os
os.makedirs("logs", exist_ok=True)

# File handler
file_handler = logging.FileHandler(f"logs/{config.LOG_FILE}")
file_handler.setLevel(getattr(logging, config.LOG_LEVEL))

# Console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(getattr(logging, config.LOG_LEVEL))

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_info(message):
    logger.info(message)

def log_error(message):
    logger.error(message)

def log_warning(message):
    logger.warning(message)

def log_debug(message):
    if config.DEBUG:
        logger.debug(message)