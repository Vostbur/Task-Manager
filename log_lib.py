import sys
import logging
import logging.handlers

LOG_FILENAME = 'logging.log'
LEVELS = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warning': logging.WARNING,
    'error': logging.ERROR,
    'critical': logging.CRITICAL,
}

level = logging.DEBUG
if len(sys.argv) > 1:
    level_name = sys.argv[1]
    level = LEVELS.get(level_name, logging.NOTSET)


def get_logger():
    app_logger = logging.getLogger(__name__)
    app_logger.setLevel(level)
    handler = logging.handlers.RotatingFileHandler(
        LOG_FILENAME,
        backupCount=10,
        maxBytes=1048576
    )
    handler.setFormatter(
        logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
    )
    app_logger.addHandler(handler)
    return app_logger


if __name__ == '__main__':
    pass
