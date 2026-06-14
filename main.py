import logging

def main():
    logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
    )

    logger = logging.getLogger(__name__)


if __name__ == "__main__":
    main()
