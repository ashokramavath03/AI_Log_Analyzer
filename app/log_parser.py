# === app/log_parser.py ===
import re

def parse_log_line(line):
    pattern = r"(?P<timestamp>\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}\.\d+) - #\d+ - \d+/\d+ - (?P<component>[\w:]+): (?P<message>.+)"
    match = re.match(pattern, line)
    if match:
        return match.groupdict()
    return None

def parse_log_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()
    return [parse_log_line(line) for line in lines if parse_log_line(line)]
