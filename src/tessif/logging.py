"""Tessif's logging specifications."""

import logging
from logging.handlers import TimedRotatingFileHandler

from tessif.frused.configurations import general_logging_level, maximum_number_of_logs
from tessif.frused.paths import logging_file

registered_logging_level_specifiers = ["debug", "info", "warning", "error", "critical"]
"""
Supported `logging levels
 <https://docs.python.org/3/library/logging.html#logging-levels>`_.
"""

registered_logging_levels = {k: k for k in registered_logging_level_specifiers}
"""
Mapping tessifs `logging level
<https://docs.python.org/3/library/logging.html#logging-levels>`_ tags to
themselves for failsafe and sanitized logging level accesss.
"""

# Define a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define a file handler to write log messages to a file
# file_handler = logging.FileHandler(logging_file)
file_handler = TimedRotatingFileHandler(
    logging_file,
    when="D",  # seperate log for each day
    backupCount=maximum_number_of_logs,  # number of files logged
    delay=True,
    errors="doRollover",
)
file_handler.setLevel(logging.DEBUG)
file_handler.doRollover()

# Define a stream handler to write log messages to the console
stream_handler = logging.StreamHandler()
stream_handler.setLevel(getattr(logging, general_logging_level.upper()))

# Define a formatter for the handlers
formatter = logging.Formatter(
    "[{levelname} - {filename} ln:{lineno}]: {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M:%S",
)

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def set_logger_level(logger, level):
    """Modify logging levels of Tessif's loggers."""
    for handler in logger.handlers:
        handler.setLevel(level)
