import json
import yaml
import os.path
from yaml.loader import SafeLoader
from gendiff.differences import make_diff
from gendiff.formatters.stylish_formatter import stylish
from gendiff.formatters.plain_formatter import plain
from gendiff.formatters.json_formatter import json_formatter


def get_file_format(filepath):
    return os.path.splitext(filepath)[1]


def read_file(filepath):
    with open(filepath, 'r') as file:
        file_content = file.read()
    return file_content


def get_dict(file_content, file_format):
    if file_format == '.json':
        data = json.loads(file_content)
    else:
        data = yaml.load(file_content, Loader=SafeLoader)
    return data


def generate_diff(filepath_1, filepath_2, formatter='stylish'):
    file_format_1 = get_file_format(filepath_1)
    file_format_2 = get_file_format(filepath_2)
    file_content_1 = read_file(filepath_1)
    file_content_2 = read_file(filepath_2)
    dict_1 = get_dict(file_content_1, file_format_1)
    dict_2 = get_dict(file_content_2, file_format_2)
    diff = make_diff(dict_1, dict_2)
    if formatter == 'stylish':
        return stylish(diff)
    elif formatter == 'plain':
        return plain(diff)
    elif formatter == 'json':
        return json_formatter(diff)
