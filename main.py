import argparse
import configparser
import os
import re

from src.log_analyzer.get_statistic import LogAnalyzerClass, write_html_with_template
from src.log_analyzer.read_file import get_filename, read_logs
from src.log_analyzer.settings import (
    DEF_CONFIG_PATH,
    DEF_LOG_DIR,
    DEF_REPORT_DIR,
    DEF_REPORT_SIZE,
)


def parse_line(line):
    log_pattern = re.compile(
        r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+(?P<user_id>\S+)\s+-\s+\[(?P<date_time>[^\]]+)\]\s+"(?P<method>\w+)\s+(?P<url>\S+)\s+HTTP/(?P<http_version>[\d.]+)"\s+'
        r'(?P<status>\d+)\s+(?P<size>\d+)\s+"(?P<referrer>.*?)"\s+"(?P<user_agent>.*?)"\s+"(?P<some_field>.*?)"\s+"(?P<another_field>.*?)"\s+(?P<request_time>[\d.]+)'
    )
    match = log_pattern.match(line)

    if match:
        data = match.groupdict()
    else:
        raise Exception("problem with parse")
    return data


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=False)
    args = parser.parse_args()

    config_path = args.config
    if config_path is None:
        config_path = DEF_CONFIG_PATH

    report_dir = DEF_REPORT_DIR
    log_dir = DEF_LOG_DIR
    report_size = DEF_REPORT_SIZE

    if not os.path.isfile(config_path):
        print(f"Файл конфигурации не найден: {config_path}")

    else:
        config = configparser.ConfigParser()
        config.read(config_path)

        report_dir = config["DEFAULT"]["REPORT_DIR"] or DEF_REPORT_DIR
        log_dir = config["DEFAULT"]["LOG_DIR"] or DEF_LOG_DIR
        report_size = int(config["DEFAULT"]["REPORT_SIZE"] or DEF_REPORT_SIZE)

    analyzer = LogAnalyzerClass()

    filename = get_filename(log_dir)
    for line_number, line in enumerate(read_logs(f"{log_dir}{os.sep}{filename}"), 1):
        # if line_number == 10000:
        #     break
        try:
            line = parse_line(line)
            analyzer.add_line(line)
        except Exception:
            pass

    statistics = analyzer.get_statistic()

    report_name = "report-" + re.search(r"\d{8}", filename).group(0) + ".html"
    write_html_with_template(statistics, report_size, rf"{report_dir}{os.sep}{report_name}")


if __name__ == "__main__":
    main()
