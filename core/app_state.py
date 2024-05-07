import logging
from functools import lru_cache

from core.config import Config

#
# class AppState:
#     value: int
#
#     @lru_cache
#     def __new__(cls):
#         """for DependsAppState"""
#         return super().__new__(cls)
#
#     @lru_cache
#     def __init__(self):
#         """if without lru_cache self.database is change always"""
#         self.value = 0
#
#     @staticmethod
#     def init_logging():
#         logging.basicConfig(
#             level=logging.getLevelName(Config.from_env().log_level),
#             datefmt='%Y/%m/%d %H:%M:%S',
#             format='%(asctime)s|%(levelname)s|%(message)s',
#         )

