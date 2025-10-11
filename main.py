import argparse
import os
import re
from datetime import datetime

from src.log_analyzer.analyzer import LogAnalyzerClass, write_html_with_template
from src.log_analyzer.file_manager import get_filename, parse_line, read_json_file, read_logs
from src.log_analyzer.settings import CONFIG, DEF_CONFIG_PATH


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, required=False)
    args = parser.parse_args()

    config_path = args.config
    if config_path is None:
        config_path = DEF_CONFIG_PATH

    config = CONFIG
    if not os.path.isfile(config_path):
        print(f"Файл конфигурации не найден: {config_path}")
    else:
        config_from_file = read_json_file(config_path)
        config.update(config_from_file)

    analyzer = LogAnalyzerClass()

    filename = get_filename(config["LOG_DIR"])
    if not filename:
        return
    for line in read_logs(f"{config['LOG_DIR']}{os.sep}{filename}"):
        # test_case
        # if line_number == 10000:
        #     break
        try:
            line = parse_line(line)
            analyzer.add_line(line)
        except Exception:
            pass

    statistics = analyzer.get_statistic()

    date_for_report = datetime.strptime(re.search(r"\d{8}", filename).group(0), "%Y%m%d").strftime("%Y.%m.%d")
    report_name = f"report-{date_for_report}.html"
    write_html_with_template(statistics, config["REPORT_SIZE"], rf"{config['REPORT_DIR']}{os.sep}{report_name}")


if __name__ == "__main__":
    main()
