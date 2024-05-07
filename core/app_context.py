import logging
import logging.config
import logging.handlers
import os

from core.config import Config


class AppContext:
    config: Config = Config.from_env()
    logger = logging.getLogger('app')

    @classmethod
    def init_logging(cls):
        os.makedirs(AppContext.config.log_dir, exist_ok=True)
        logging_cfg = {
            'version': 1,
            'formatters': {
                'simple': {'format': '[%(name)s] %(message)s'},
                'complex': {
                    'format': '%(asctime)s|%(levelname)s|%(name)s|%(filename)s:%(lineno)d|%(message)s'
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'complex',
                    'level': 'DEBUG',
                },
                'rolling_file': {
                    'level': 'DEBUG',
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': AppContext.config.log_dir + '/app.log',
                    'maxBytes': 1024 * 1024 * 5,  # 5 MB
                    'backupCount': 5,
                    'formatter': 'complex',
                },
                'file': {
                    'class': 'logging.FileHandler',
                    'filename': 'error.log',
                    'formatter': 'complex',
                    'level': 'ERROR',
                },
            },
            'loggers': {
                'app': {
                    'handlers': ['console', 'rolling_file'],
                    'level': AppContext.config.log_level,
                }
            },
        }
        logging.config.dictConfig(logging_cfg)
