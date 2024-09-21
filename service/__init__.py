"""
Package: service
Package for the application models and service routes.
This module creates and configures the Flask app and sets up the logging
and SQL database.
"""

import sys
from flask import Flask
from service import config
from service.common import log_handlers
from flask_talisman import Talisman
from flask_cors import CORS

# Create Flask application
app = Flask(__name__)

# Enable security features with Talisman and cross-origin support with CORS
talisman = Talisman(app, force_https=False)
CORS(app)

# Load configuration from the config module
app.config.from_object(config)

# Import routes and models after creating the Flask app
# pylint: disable=wrong-import-position, cyclic-import, wrong-import-order
from service import routes, models  # noqa: F401 E402

# Import common error handlers and CLI commands
# pylint: disable=wrong-import-position
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Set up logging for production
log_handlers.init_logging(app, "gunicorn.error")

# Log that the service has started
app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

# Initialize the database
try:
    models.init_db(app)  # Make our database tables
except Exception as error:  # pylint: disable=broad-except
    app.logger.critical("%s: Cannot continue", error)
    # Gunicorn requires exit code 4 to stop spawning workers when they die
    sys.exit(4)

# Log service initialization completion
app.logger.info("Service initialized!")
