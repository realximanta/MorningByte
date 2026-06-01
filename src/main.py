"""
main.py — MorningByte entry point.

Detects whether it's a morning or evening run via the MORNINGBYTE_PUSH
environment variable, gathers data from each module, builds the message,
and sends it to Telegram.

Usage:
    MORNINGBYTE_PUSH=morning python main.py
    MORNINGBYTE_PUSH=evening python main.py
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path

# Allow running from repo root or src/
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

from news import get_headlines
from telegram import (
    build_evening_message,
    build_morning_message,
    send_message,
)
from weather import get_weather
from wikipedia import get_random_fact

# ── Logging ──────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("morningbyte")

# ── Config ────────────────────────────────────────────────────────────────────
# Default location: Nagaon, Assam, India — change to your city.
DEFAULT_CITY = os.getenv("CITY_NAME", "Nagaon")
DEFAULT_LAT = float(os.getenv("CITY_LAT", "26.3474"))
DEFAULT_LON = float(os.getenv("CITY_LON", "92.6843"))
NEWS_COUNTRY = os.getenv("NEWS_COUNTRY", "us")


def format_date() -> str:
    """Return a nicely formatted date string, e.g. '02 June 2026'."""
    return datetime.now().strftime("%d %B %Y")


def run_morning() -> None:
    """Collect data and send the morning briefing."""
    logger.info("Starting morning push…")

    date_str = format_date()
    weather = get_weather(DEFAULT_LAT, DEFAULT_LON, DEFAULT_CITY)
    headlines = get_headlines(country=NEWS_COUNTRY, count=3)
    fact = get_random_fact()

    message = build_morning_message(date_str, weather, headlines, fact)
    success = send_message(message)

    if success:
        logger.info("Morning push complete ✓")
    else:
        logger.error("Morning push FAILED")
        sys.exit(1)


def run_evening() -> None:
    """Collect data and send the evening briefing."""
    logger.info("Starting evening push…")

    date_str = format_date()
    headlines = get_headlines(country=NEWS_COUNTRY, count=3)
    fact = get_random_fact()

    message = build_evening_message(date_str, headlines, fact)
    success = send_message(message)

    if success:
        logger.info("Evening push complete ✓")
    else:
        logger.error("Evening push FAILED")
        sys.exit(1)


def main() -> None:
    load_dotenv()  # Load .env file when running locally

    push_type = os.getenv("MORNINGBYTE_PUSH", "").strip().lower()

    if push_type == "morning":
        run_morning()
    elif push_type == "evening":
        run_evening()
    else:
        logger.error(
            "MORNINGBYTE_PUSH must be 'morning' or 'evening'. Got: '%s'",
            push_type,
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
