import logging


def setup_logger(logging_level: int | str | None = None) -> logging.Logger:
    if logging_level is None:
        logging_level = logging.ERROR
    logger = logging.getLogger()
    logger.setLevel(logging_level)
    ch = logging.StreamHandler()
    ch.setLevel(logging_level)
    formatter = logging.Formatter("%(levelname)s | %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger
