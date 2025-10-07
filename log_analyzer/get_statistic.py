import re
import statistics
import json
import os
from datetime import datetime
from msilib.schema import tables


class LogAnalyzerClass():
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
                "count_perc": round(100*info["count"]/self.count_lines,3),
                "time_sum": round(time_sum,3),
                "time_perc": round(100*time_sum/self.all_requests_time,3),
                "time_avg": round(time_sum/self.log_info[url]["count"],3),
                "time_max": max(info["times"]),
                "time_med": round(statistics.median(info["times"]),3)

            }
            self.log_info[url] = new_value

        self.log_info = sorted(self.log_info.values(), key=lambda x: x["time_sum"], reverse=True)


    def get_statistic(self):
        self._calculate_statistics()
        return self.log_info
        # for line in self.log_info:
        #     yield line






def write_html_with_template(json_data, template_path="data/report.html", output_file="report.html"):

    with open(template_path, "r", encoding="utf-8") as template_file:
        template_content = template_file.read()
    
    max_rows = 2
    json_str = json.dumps(json_data[:max_rows], ensure_ascii=False, indent=2)
    html_content = template_content.replace("$table_json", json_str)
    

    with open(output_file, "w", encoding="utf-8") as output:
        output.write(html_content)
    
    print(f"HTML отчет сохранен в: {output_file}")
    return output_file

