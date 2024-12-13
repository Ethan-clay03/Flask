import logging

# Define logging formats
LOG_FORMAT = '%(asctime)s %(name)s : %(levelname)s - %(message)s'

# Define log levels
LOG_LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

# Default log directory
LOG_DIR = 'logs'
