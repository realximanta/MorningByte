import logging
import os
import requests
from typing import Optional

logger = logging.getLogger(__name__)

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"


def get_headlines(
    country: str = "us",
    count: int = 3,
) -> Optional[list[str]]:
    api_key = os.getenv("NEWSAPI_KEY")
    if not api_key:
        logger.error("NEWSAPI_KEY not set in environment.")
        return None

    params = {
        "country": country,
        "pageSize": count,
        "apiKey": api_key,
    }

    try:
        response = requests.get(NEWSAPI_URL, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        articles = data.get("articles", [])
        if not articles:
            logger.warning("No articles returned from NewsAPI.")
            return None

        headlines = [
            article["title"]
            for article in articles[:count]
            if article.get("title") and article["title"] != "[Removed]"
        ]

        logger.info("Fetched %d headlines.", len(headlines))
        return headlines

    except requests.RequestException as e:
        logger.error("Failed to fetch headlines: %s", e)
        return None
