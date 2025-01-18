import sys

from loguru import logger


def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level="INFO",
               format="{time} {level} {message}", backtrace=True, diagnose=True)
    logger.add(sys.stdout, level="WARNING",
               format="{time} {level} {message}", backtrace=True, diagnose=True)
    logger.add(sys.stderr, level="ERROR",
               format="{time} {level} {message}", backtrace=True, diagnose=True)
