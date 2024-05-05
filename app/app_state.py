import logging
from dataclasses import dataclass

from app.config import Config


@dataclass
class AppState:
    config: Config

    def init_logging(self):
        logging.basicConfig(
            level=logging.getLevelName(self.config.log_level),
            datefmt='%Y/%m/%d %H:%M:%S',
            format='%(asctime)s|%(levelname)s|%(message)s',
        )
