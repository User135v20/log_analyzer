from log_analyzer.get_statistic import *
from log_analyzer.read_file import _read

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
    analyzer = LogAnalyzerClass()

    #добавление данных
    for line_number, line in enumerate(_read(), 1):

        # if line_number == 10000:
        #     break
        try:
            line = parse_line(line)
            analyzer.add_line(line)
        except:
            pass



    # Генерируем JSON данные
    write_html_with_template(analyzer.get_statistic())

if __name__ == "__main__":
    main()
