"""Tessif's logging specifications."""

import logging
from logging.handlers import TimedRotatingFileHandler

from tessif.frused.configurations import general_logging_level, maximum_number_of_logs
from tessif.frused.paths import logging_file


def create_file_handler():
    """Create a tessif style logging file handler."""
    # Define a file handler to write log messages to a file

    file_handler = TimedRotatingFileHandler(
        logging_file,
        when="D",  # seperate log for each day
        backupCount=maximum_number_of_logs,  # number of files logged
        delay=True,
    )
    file_handler.setLevel(logging.DEBUG)
    # file_handler.doRollover()

    file_formatter = logging.Formatter(
        "[{asctime} {levelname} - {filename} ln:{lineno}]: {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(file_formatter)

    return file_handler


def create_stream_handler():
    """Create a (currently unused) tessif style logging stream handler."""
    # Define a stream handler to write log messages to the console

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(getattr(logging, general_logging_level.upper()))

    stream_formatter = logging.Formatter(
        "[{levelname}]: {message}",
        # "[{levelname} - {filename} ln:{lineno}]: {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    stream_handler.setFormatter(stream_formatter)

    return stream_handler


def create_logger(name):
    """Create a tessif-style logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    reset_basic_config()

    # Add the handlers to the logger
    logger.addHandler(create_file_handler())
    # logger.addHandler(create_stream_handler())

    return logger


def reset_stream_handler(logger):
    """Reset a loggers stream handler.

    Usefull when tropping using tessif.system_model.tropp.

    Parameters
    ----------
    logger:
        Logger of which the stream handler is to be reset
    """
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            logger.removeHandler(handler)

    logger.addHandler(create_stream_handler())

    return logger


def reset_basic_config():
    """Reset the logging modules basic configuration.

    Particularly useful when third party modules overwrite basic config.
    """
    logging.basicConfig(
        format="[{levelname}]: {message}",
        style="{",
        level=logging.WARNING,
        force=True,
    )
