"""
telegram.py — Sends formatted HTML messages via Telegram Bot API.
"""

import logging
import os
import requests
from typing import Optional

logger = logging.getLogger(__name__)


def send_message(text: str) -> bool:
    """
    Send an HTML-formatted message to a Telegram chat.

    Args:
        text: HTML-formatted message string (supports <b>, <i>, <code>, etc.)

    Returns:
        True if message was sent successfully, False otherwise.
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        logger.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set.")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("Telegram message sent successfully.")
        return True

    except requests.RequestException as e:
        logger.error("Failed to send Telegram message: %s", e)
        return False


def build_morning_message(
    date_str: str,
    weather: Optional[dict],
    headlines: Optional[list[str]],
    fact: Optional[dict],
) -> str:
    """
    Build the morning HTML message.

    Args:
        date_str: Formatted date string.
        weather: Dict with city, temperature, condition — or None.
        headlines: List of headline strings — or None.
        fact: Dict with title, extract — or None.

    Returns:
        Formatted HTML string.
    """
    lines: list[str] = []

    lines.append("☀️ <b>MorningByte</b>")
    lines.append("")
    lines.append(f"📅 {date_str}")
    lines.append("")

    # Weather
    if weather:
        lines.append(f"🌤 <b>{weather['city']}</b>")
        lines.append(f"{weather['temperature']}°C • {weather['condition']}")
    else:
        lines.append("🌤 Weather unavailable")
    lines.append("")

    # Headlines
    lines.append("📰 <b>Headlines</b>")
    if headlines:
        for i, headline in enumerate(headlines, 1):
            lines.append(f"{i}. {headline}")
    else:
        lines.append("Headlines unavailable.")
    lines.append("")

    # Wikipedia
    lines.append("📚 <b>Wikipedia</b>")
    if fact:
        lines.append(f"<i>{fact['title']}</i>")
        lines.append(fact["extract"])
    else:
        lines.append("Fact unavailable.")
    lines.append("")

    lines.append("🚀 Time to build.")

    return "\n".join(lines)


def build_evening_message(
    date_str: str,
    headlines: Optional[list[str]],
    fact: Optional[dict],
) -> str:
    """
    Build the evening HTML message.

    Args:
        date_str: Formatted date string.
        headlines: List of headline strings — or None.
        fact: Dict with title, extract — or None.

    Returns:
        Formatted HTML string.
    """
    lines: list[str] = []

    lines.append("🌙 <b>EveningByte</b>")
    lines.append("")
    lines.append(f"📅 {date_str}")
    lines.append("")

    # Headlines
    lines.append("📰 <b>Headlines</b>")
    if headlines:
        for i, headline in enumerate(headlines, 1):
            lines.append(f"{i}. {headline}")
    else:
        lines.append("Headlines unavailable.")
    lines.append("")

    # Wikipedia
    lines.append("📚 <b>Wikipedia</b>")
    if fact:
        lines.append(f"<i>{fact['title']}</i>")
        lines.append(fact["extract"])
    else:
        lines.append("Fact unavailable.")
    lines.append("")

    lines.append("✨ See you tomorrow.")

    return "\n".join(lines)
