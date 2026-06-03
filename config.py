"""
Configuration for UK Sky Carrier Lookup System
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Browser Settings
HEADLESS_MODE = True  # Set to False for debugging
BROWSER_WINDOW_SIZE = (1920, 1080)

# Delays & Timeouts (in seconds)
DELAY_BETWEEN_REQUESTS = 8  # Wait time between each lookup
PAGE_LOAD_TIMEOUT = 30
CAPTCHA_TIMEOUT = 60  # How long to wait for CAPTCHA solving

# Retry Configuration
RETRY_ATTEMPTS = 3
RETRY_DELAY = 5  # seconds between retries

# Target Website
TARGET_URL = "https://www.freecarrierlookup.com"

# Filter Settings
TARGET_CARRIER = "Sky UK Limited"  # Only return this carrier
ENABLED_FILTERING = True

# Logging
LOG_FILE = "lookup.log"
LOG_LEVEL = "INFO"

# Output
OUTPUT_DIRECTORY = "results"
CSV_COLUMNS = ["phone_number", "carrier", "status", "timestamp"]

# User Agent (to avoid detection)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# Proxy (optional - leave empty if not using)
PROXY = os.getenv("PROXY_URL", "")

# Debug Mode
DEBUG = os.getenv("DEBUG", "False").lower() == "true"