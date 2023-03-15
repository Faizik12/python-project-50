import json
import yaml
from yaml.loader import SafeLoader
from gendiff.differences import make_diff
from gendiff.formatters.stylish_formatter import stylish
from gendiff.formatters.plain_formatter import plain
from gendiff.formatters.json_formatter import json_formatter


def read_file(filepath):
    json_format = 'json'
    yaml_format = 'yaml'
    with open(filepath, 'r') as file_1:
        if filepath.endswith('.json'):
            data = (file_1.read(), json_format)
        else:
            data = (file_1.read(), yaml_format)
    return data


def get_dict(data_1, data_2):
    text_1, format_1 = data_1
    text_2, format_2 = data_2
    if format_1 == 'json':
        dict_1 = json.loads(text_1)
    else:
        dict_1 = yaml.load(text_1, Loader=SafeLoader)
    if format_2 == 'json':
        dict_2 = json.loads(text_2)
    else:
        dict_2 = yaml.load(text_2, Loader=SafeLoader)
    return (dict_1, dict_2)


def generate_diff(filepath_1, filepath_2, formatter='stylish'):
    data_1 = read_file(filepath_1)
    data_2 = read_file(filepath_2)
    dict_1, dict_2 = get_dict(data_1, data_2)
    diff = make_diff(dict_1, dict_2)
    if formatter == 'stylish':
        return stylish(diff)
    elif formatter == 'plain':
        return plain(diff)
    elif formatter == 'json':
        return json_formatter(diff)
