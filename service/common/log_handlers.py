"""
Log Handlers

This module contains utility functions to set up logging consistently.
"""

import logging
import sys


def init_logging(app, logger_name: str):
    """Set up logging for production"""
    app.logger.propagate = (
        False  # Prevent log messages from being passed to the root logger
    )

    # Retrieve the Gunicorn logger
    gunicorn_logger = logging.getLogger(logger_name)

    # Attach Gunicorn handlers to the Flask app's logger
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    # Define a consistent log format
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] " "[%(module)s] %(message)s"
    )

    # Apply the formatter to all handlers associated with the Flask app's logger
    for handler in app.logger.handlers:
        handler.setFormatter(formatter)

    # Optionally, add a console handler if needed for debugging
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)

    app.logger.info("Logging handler established")
