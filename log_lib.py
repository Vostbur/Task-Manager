"""USAGE module log_lib.py:
create your_app.py with:

    import log_lib
    app_logger = log_lib.get_logger('filename.log')
    app_logger.debug('Start logging...')

Change logging level from command line args:

    python your_app.py info
"""

import sys
import logging
import logging.handlers


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


def get_logger(log_filename):
    app_logger = logging.getLogger(log_filename)
    app_logger.setLevel(level)
    handler = logging.handlers.RotatingFileHandler(
        log_filename,
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
