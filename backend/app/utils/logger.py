# utils/logger.py
import logging

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.hasHandlers():
        logger.setLevel(logging.DEBUG)

        # Console Handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        ch.setFormatter(formatter)

        logger.addHandler(ch)

    return logger
