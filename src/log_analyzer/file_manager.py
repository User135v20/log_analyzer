import gzip
import json
import re
from datetime import datetime
from inspect import signature
from pathlib import Path


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


def extract_date(filename):
    match = re.search(r"(\d{8})(\.\w+)?$", filename)
    if match:
        date_str = match.group(1)
        try:
            return datetime.strptime(date_str, "%Y%m%d")
        except ValueError:
            return None
    return None


def get_filename(dir_name):
    directory_path = Path(dir_name)
    max_date = datetime.min
    for el in directory_path.iterdir():
        if not (el.is_file() and el.name.startswith("nginx-access-ui")):
            continue

        date_for_file = extract_date(el.name)
        if date_for_file > max_date:
            file = el.name
            max_date = date_for_file

    if file is None:
        raise FileNotFoundError(f"No file found at {dir_name}")

    return file


def check_file(arg_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            sig = signature(func)
            params = sig.bind(*args, **kwargs)
            params.apply_defaults()
            file_path = Path(params.arguments[arg_name])
            if not file_path.exists():
                raise FileNotFoundError(f"No file found at {file_path}")
            return func(*args, **kwargs)

        return wrapper

    return decorator


@check_file("file_path")
def read_gz_line_by_line(file_path):
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for line in f:
            yield line.strip()


@check_file("file_path")
def read_file_line_by_line(file_path):
    with open(file_path, encoding="utf-8") as file:
        for line in file:
            yield line.strip()


@check_file("file_path")
def read_file(file_path):
    with open(file_path, encoding="utf-8") as file:
        return file.read()


def read_json_file(file_path):
    with open(file_path, encoding="utf-8") as file:
        return json.load(file)


def read_logs(file_path: str):
    if file_path.endswith("gz"):
        return read_gz_line_by_line(file_path)
    else:
        return read_file_line_by_line(file_path)


def write_file(file_path, data):
    with open(file_path, "w", encoding="utf-8") as output:
        output.write(data)
