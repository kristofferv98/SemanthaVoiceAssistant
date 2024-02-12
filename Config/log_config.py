import logging.config
import json
from pathlib import Path
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

LOG_FORMAT = "%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s — %(pathname)s"


def setup_logging(default_path: str = 'logging.json', default_level: int = logging.INFO,
                  env_key: str = 'LOG_CFG') -> None:
    """
    Setup logging configuration from a JSON file.

    :param default_path: Default JSON file path for logging configuration.
    :param default_level: Default logging level.
    :param env_key: Environment variable key for logging configuration file path.
    """
    path = Path(os.getenv(env_key, default_path))
    if path.is_file():
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)  # Changed to default_level


def get_logger(log_level: str = 'INFO') -> logging.Logger:
    """
    Retrieve a configured logger with the specified log level.

    :param log_level: The log level for the logger. Defaults to 'INFO'.
    :return: Configured logger.
    """
    # Convert log level to upper case to allow for string input 'info' or 'INFO'
    log_level = log_level.upper()  # Changes to log_level.upper()

    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Check if the console handler already exists to prevent duplicate logs
    if not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        formatter = logging.Formatter(LOG_FORMAT)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # Ensure 'pyautogen' logger does not show warnings by setting its level to ERROR
    semantic_router_logger = logging.getLogger("semantic_router.utils.logger")
    semantic_router_logger.setLevel(logging.WARNING)

    return logger
