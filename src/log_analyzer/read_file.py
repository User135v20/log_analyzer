import gzip
import re
from datetime import datetime
from pathlib import Path


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


def read_logs(file_path):
    with gzip.open(file_path, "rt", encoding="utf-8") as f:
        for line in f:
            yield line.strip()
