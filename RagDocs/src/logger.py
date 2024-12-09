import os
import logging
from time import time_ns
from logging import Logger as SuperLogger
from logging.handlers import RotatingFileHandler

if not os.path.exists("./Logs"):
    os.mkdir("./Logs")


class Logger(SuperLogger):
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    DEBUG = logging.DEBUG

    latency_timer = 0

    def start_latency_timer(self):
        self.latency_timer = time_ns()

    def log_latency(self, pre_message: str):
        self.debug(
            f"{pre_message}: {(time_ns() - self.latency_timer)/(1000000)} ms latency"
        )
        self.start_latency_timer()

    def __init__(self, name: str = "root"):
        super().__init__(name)

        self.logger = logging.getLogger(name)
        log_formatter = logging.Formatter(
            "[%(asctime)s] %(name)s | %(filename)s->%(funcName)s():%(lineno)s | %(process)d %(thread)d %(taskName)s | %(levelname)s: %(message)s"
        )
        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(log_formatter)
        self.addHandler(consoleHandler)

        # Create a Handler to send logs to File
        # File Max Size is 10 MB, after reaching it. It creates a new file. Max 10 files can exist.
        fileHandler = RotatingFileHandler(
            "./Logs/logs.log", backupCount=10, maxBytes=10000000
        )
        fileHandler.setFormatter(log_formatter)
        # add file handler to the root logger
        self.addHandler(fileHandler)

        if os.environ.get("ENV", "dev").lower() == "dev":
            self.setLevel(logging.DEBUG)
        else:
            self.setLevel(logging.DEBUG)
