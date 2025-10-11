import argparse
import os
import re
from datetime import datetime

from src.log_analyzer.analyzer import LogAnalyzerClass, write_html_with_template
from src.log_analyzer.file_manager import check_file, get_filename, parse_line, read_json_file, read_logs
from src.log_analyzer.settings import CONFIG, DEF_CONFIG_PATH, configure_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=False)
    args = parser.parse_args()

    config_path = args.config
    if config_path is None:
        config_path = DEF_CONFIG_PATH

    config = CONFIG
    try:
        config_from_file = read_json_file(config_path)
        config.update(config_from_file)
    except Exception as e:
        raise Exception(f"Failed to read config file. path: {config_path}") from e

    logger = configure_logger(config["ANALYZER_LOGS"])
    logger.info("log analysis started.")
    analyzer = LogAnalyzerClass()

    filename = get_filename(config["LOG_DIR"])
    if not filename:
        return
    date_for_report = datetime.strptime(re.search(r"\d{8}", filename).group(0), "%Y%m%d").strftime("%Y.%m.%d")
    report_name = f"report-{date_for_report}.html"
    if check_file(rf"{config['REPORT_DIR']}{os.sep}{report_name}"):
        logger.info(f"Report {report_name} already exists.")
        return

    count = 0
    problem_lines = 0
    for line in read_logs(f"{config['LOG_DIR']}{os.sep}{filename}"):
        count += 1
        line = parse_line(line)
        if line:
            analyzer.add_line(line)
        else:
            problem_lines += 1

    if problem_lines / count > 0.5:
        logger.error(f"most of the analyzed the log ({round(problem_lines / count, 2)}) could not be parsed.")

    statistics = analyzer.get_statistic()
    write_html_with_template(statistics, config["REPORT_SIZE"], rf"{config['REPORT_DIR']}{os.sep}{report_name}")


if __name__ == "__main__":
    main()
