import logging
from dataclasses import dataclass
from typing import Any

from _app.database import Database


@dataclass
class AppState:
    config: Any
    database: Database

    def __init__(self, config: Any):
        self.config = config
        self.database = Database(config)

    def init_logging(self):
        logging.basicConfig(
            level=logging.getLevelName(self.config.log_level),
            datefmt='%Y/%m/%d %H:%M:%S',
            format='%(asctime)s|%(levelname)s|%(message)s',
        )



