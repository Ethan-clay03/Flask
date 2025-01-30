import logging
import os
from .config import LOG_FORMAT, LOG_LEVELS, LOG_DIR

class LoggerConfig:
    def __init__(self, logs_dir=LOG_DIR):
        self.logs_dir = logs_dir
        self.ensure_logs_dir_exists()

    def ensure_logs_dir_exists(self):
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)

    def setup_logger(self, name, log_file='error.log', level=logging.DEBUG):
        log_file_path = os.path.join(self.logs_dir, log_file)
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        file_handler = logging.FileHandler(log_file_path)
        console_handler = logging.StreamHandler()
        
        file_handler.setLevel(level)
        console_handler.setLevel(level)
        
        formatter = logging.Formatter(LOG_FORMAT)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        return logger

# Create different loggers here
logger_config = LoggerConfig()
app_logger = logger_config.setup_logger('app', log_file='app.log', level=LOG_LEVELS['debug'])
db_logger = logger_config.setup_logger('db', log_file='db.log', level=LOG_LEVELS['info'])
auth_logger = logger_config.setup_logger('auth', log_file='auth.log', level=LOG_LEVELS['debug'])
error_logger = logger_config.setup_logger('error', log_file='error.log', level=LOG_LEVELS['debug'])
debug_logger = logger_config.setup_logger('debug', log_file='debug.log', level=LOG_LEVELS['debug'])
