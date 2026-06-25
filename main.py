import logging
import colorlog
import requests
import os
import dotenv
from getdata import fetch_activity
from twitter import getTweetsByRepo

import os
from datetime import datetime

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

logger = logging.getLogger(__name__)
dotenv.load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_to_telegram(message):
    if not BOT_TOKEN or not CHAT_ID:
        logger.warning("telegram credentials not set, skipping")
        return
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        })
        logger.info(f"sent to telegram")
    except Exception as e:
        logger.error(f"telegram send failed: {e}")

def main():
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s [%(levelname)s]%(reset)s %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red"
        }
    ))
    logging.basicConfig(
        level=logging.DEBUG,
        handlers=[handler, logging.FileHandler(log_file)],
        format="%(asctime)s %(levelname)s %(message)s"
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

    logger.info("starting commitcast")

    activity = fetch_activity()
    tweets = getTweetsByRepo(activity)

    for (repo, date), tweet in tweets.items():
        if tweet and tweet.strip() != "SKIP":
            print(f"\n--- {repo} ({date}) ---\n{tweet}")
            send_to_telegram(f"*{repo}* — {date}\n\n{tweet}")

if __name__ == "__main__":
    main()
