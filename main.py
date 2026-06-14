import logging
import colorlog
from getdata import fetch_activity

def main():
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)s%(reset)s %(message)s",
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
        handlers=[
            handler,
            logging.FileHandler("logs/commitcast.log")
        ],
        format="%(asctime)s %(levelname)s %(message)s"
    )

    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)

    logger = logging.getLogger(__name__)
    activity = fetch_activity()
    logger.info("Starting main function")

if __name__ == "__main__":
    main()

