import logging
import os

import structlog

logging.basicConfig(level=logging.INFO, format="%(message)s", filename="my_logs.log", filemode="a")

structlog.configure(
    processors=[structlog.processors.TimeStamper(fmt="iso"), structlog.processors.JSONRenderer()],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


DEF_CONFIG_PATH = "config.json"
DEF_REPORT_DIR = "data"
DEF_LOG_DIR = "data"
DEF_REPORT_SIZE = 100

TEMPLATE_PATH = f"src{os.sep}log_analyzer{os.sep}template{os.sep}report.html"

CONFIG = {"REPORT_DIR": DEF_REPORT_DIR, "LOG_DIR": DEF_LOG_DIR, "REPORT_SIZE": DEF_REPORT_SIZE}
