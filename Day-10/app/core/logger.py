import logging
import sys

def setup_logger():
    # Create a custom logger
    logger = logging.getLogger("fastapi_app")
    logger.setLevel(logging.DEBUG) # Capture everything from DEBUG and above

    # Create handlers (Console output)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    log_format = logging.Formatter(
        "%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s:%(lineno)d) - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(log_format)

    # Add handlers to the logger
    if not logger.handlers:
        logger.addHandler(console_handler)

    return logger

logger = setup_logger()