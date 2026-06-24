import logging
import requests
from typing import Optional

logger = logging.getLogger(__name__)

WIKIPEDIA_URL = "https://en.wikipedia.org/api/rest_v1/page/random/summary"


def get_random_fact(max_chars: int = 280) -> Optional[dict]:
    headers = {
        "User-Agent": "MorningByte/1.0 (https://github.com/yourusername/MorningByte)"
    }

    try:
        response = requests.get(WIKIPEDIA_URL, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        title = data.get("title", "Unknown")
        extract = data.get("extract", "")

        if len(extract) > max_chars:
            trimmed = extract[:max_chars]
            last_period = trimmed.rfind(".")
            extract = trimmed[:last_period + 1] if last_period != -1 else trimmed + "…"

        if not extract:
            logger.warning("Empty extract from Wikipedia.")
            return None

        logger.info("Wikipedia fact fetched: '%s'", title)
        return {
            "title": title,
            "extract": extract,
        }

    except requests.RequestException as e:
        logger.error("Failed to fetch Wikipedia fact: %s", e)
        return None
