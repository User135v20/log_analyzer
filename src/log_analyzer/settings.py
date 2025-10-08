import os

DEF_CONFIG_PATH = "config.json"
DEF_REPORT_DIR = "data"
DEF_LOG_DIR = "data"
DEF_REPORT_SIZE = 100

TEMPLATE_PATH = f"src{os.sep}log_analyzer{os.sep}template{os.sep}report.html"

CONFIG = {"REPORT_DIR": DEF_REPORT_DIR, "LOG_DIR": DEF_LOG_DIR, "REPORT_SIZE": DEF_REPORT_SIZE}
