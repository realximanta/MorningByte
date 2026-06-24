import logging
import os
import sys
from datetime import datetime
from pathlib import Path

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

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("morningbyte")

DEFAULT_CITY = os.getenv("CITY_NAME", "Nagaon")
DEFAULT_LAT = float(os.getenv("CITY_LAT", "26.3474"))
DEFAULT_LON = float(os.getenv("CITY_LON", "92.6843"))
NEWS_COUNTRY = os.getenv("NEWS_COUNTRY", "in")


def format_date() -> str:
    return datetime.now().strftime("%d %B %Y")


def run_morning() -> None:
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
    load_dotenv()
    
    push_type = os.getenv("MORNINGBYTE_PUSH", "").strip().lower()
    
    logger.info("Push type: %s", push_type)
    logger.info(
        "Config: city=%s lat=%s lon=%s country=%s",
        DEFAULT_CITY,
        DEFAULT_LAT,
        DEFAULT_LON,
        NEWS_COUNTRY,
    )
    
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
