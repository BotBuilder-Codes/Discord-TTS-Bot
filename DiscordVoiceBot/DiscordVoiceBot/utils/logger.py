import logging
from config import LOG_FORMAT, LOG_LEVEL

def setup_logger(name):
    """Configure and return a logger instance"""
    logger = logging.getLogger(name)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.getLevelName(LOG_LEVEL))
    
    # Create formatter
    formatter = logging.Formatter(LOG_FORMAT)
    console_handler.setFormatter(formatter)
    
    # Add handler to logger
    logger.addHandler(console_handler)
    logger.setLevel(logging.getLevelName(LOG_LEVEL))
    
    return logger
