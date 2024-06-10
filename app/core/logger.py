import logging
import logging.config
from colorama import Fore, Style, init
from app.utils.constants import APP_LOG_LEVEL
import uvicorn

# Initialize colorama
init(autoreset=True)


class LoggingFormatter(logging.Formatter):
    # Define color codes for different log levels
    LOG_COLORS = {
        logging.DEBUG: Fore.BLUE,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT,
    }

    def format(self, record):
        log_color = self.LOG_COLORS.get(record.levelno, "")
        name_color = Fore.CYAN
        line_color = Fore.MAGENTA
        logger_color = Fore.YELLOW
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        record.filename = f"{name_color}{record.filename}{Style.RESET_ALL}"
        record.lineno = f"{line_color}{record.lineno}{Style.RESET_ALL}"
        record.name = f"{logger_color}{record.name}{Style.RESET_ALL}"
        return super().format(record)


def logging_formatter_factory():
    return LoggingFormatter(
        "%(levelname)s: logger: %(name)s [in %(filename)s: %(lineno)s]: %(message)s"
    )


# Define a custom logging configuration
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            format: "%(levelname)s: %(name)s: %(message)s",
        },
        "iap_formatter": {
            "()": logging_formatter_factory,
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "iap": {
            "formatter": "iap_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "yfinance": {
            "handlers": ["iap"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["iap"],
            "level": "INFO",
            "propagate": True,
        },
    },
}

# Apply the logging configuration
logging.config.dictConfig(logging_config)

# # Define a custom logging format
# log_format = "%(levelname)s:    %(name)s:     %(message)s"

# # Define handler
# console_handler = logging.StreamHandler()
# console_handler.setFormatter(LoggingFormatter(log_format))

# iap_logger = logging.getLogger(__name__)
# iap_logger.setLevel(APP_LOG_LEVEL)

# iap_logger.addHandler(console_handler)

# Using the uvicorn logger since uvicorn repeats the messages from custom logger
iap_logger = logging.getLogger("uvicorn.error")
