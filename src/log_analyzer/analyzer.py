import json
import statistics

from src.log_analyzer.file_manager import read_file, write_file
from src.log_analyzer.settings import TEMPLATE_PATH


class LogAnalyzerClass:
    def __init__(self):
        self.count_lines = 0
        self.all_requests_time = 0
        self.log_info = {}

    def add_line(self, line):
        url = line["url"]
        request_time = float(line["request_time"])

        self.count_lines += 1
        self.all_requests_time += request_time

        if url not in self.log_info:
            self.log_info[url] = {
                "count": 0,
                "times": [],
                "url": url,
            }

        self.log_info[url]["count"] += 1
        self.log_info[url]["times"].append(request_time)

    def _calculate_statistics(self):
        for url, info in self.log_info.items():
            time_sum = sum(info["times"])

            new_value = {
                "url": url,
                "count": info["count"],
                "count_perc": round(100 * info["count"] / self.count_lines, 3),
                "time_sum": round(time_sum, 3),
                "time_perc": round(100 * time_sum / self.all_requests_time, 3),
                "time_avg": round(time_sum / self.log_info[url]["count"], 3),
                "time_max": max(info["times"]),
                "time_med": round(statistics.median(info["times"]), 3),
            }
            self.log_info[url] = new_value

        self.log_info = sorted(self.log_info.values(), key=lambda x: x["time_sum"], reverse=True)

    def get_statistic(self):
        self._calculate_statistics()
        return self.log_info


def write_html_with_template(json_data, max_rows, output_file):
    from src.log_analyzer.settings import logger

    template_content = read_file(TEMPLATE_PATH)
    json_str = json.dumps(json_data[:max_rows], ensure_ascii=False, indent=2)
    html_content = template_content.replace("$table_json", json_str)
    write_file(output_file, html_content)
    logger.info(f"HTML отчет сохранен в: {output_file}")
    return output_file
