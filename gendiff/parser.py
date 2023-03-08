import yaml
import json
from gendiff.differences import make_diff
from gendiff.formatters.stylish_formatter import stylish
from gendiff.formatters.plain_formatter import plain
from yaml.loader import SafeLoader


def generate_diff(filepath_1, filepath_2, formatter='stylish'):
    with open(filepath_1, 'r') as file_1:
        with open(filepath_2, 'r') as file_2:
            if filepath_1.endswith('.json'):
                data_1 = json.load(file_1)
            else:
                data_1 = yaml.load(file_1, Loader=SafeLoader)
            if filepath_2.endswith('.json'):
                data_2 = json.load(file_2)
            else:
                data_2 = yaml.load(file_2, Loader=SafeLoader)
    diff = make_diff(data_1, data_2)
    if formatter == 'stylish':
        return stylish(diff)
    elif formatter == 'plain':
        return plain(diff)
    elif formatter == 'json':
        return json.dumps(diff, indent=4)
