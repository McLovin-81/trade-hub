import logging
from logging.handlers import RotatingFileHandler


SECRET_KEY = 'supersecretkey'
DATABASE = 'instance/trade_hub_database.sqlite'

#SQLALCHEMY_DATABASE_URI = 'sqlite:///instance/database.db'
#DEBUG = True

# Logging configuration
LOG_FILE = 'instance/logs/app.log'
LOG_LEVEL = logging.INFO
LOG_MAX_BYTES = 100000
LOG_BACKUP_COUNT = 3

# Define your logging configuration function
def configure_logging(app):
    if not app.debug:
        # Create a file handler for logging
        handler = RotatingFileHandler(LOG_FILE, maxBytes=LOG_MAX_BYTES, backupCount=LOG_BACKUP_COUNT)
        handler.setLevel(LOG_LEVEL)

        # Define the logging format
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        handler.setFormatter(formatter)

        # Add the handler to the app's logger
        app.logger.addHandler(handler)
        app.logger.setLevel(LOG_LEVEL)

        # Log that the application has started
        app.logger.info('Application startup')