import yaml
import json
from itertools import chain
from yaml.loader import SafeLoader


def make_right(data):
    if isinstance(data, bool):
        return 'true' if data else 'false'
    return data


def get_string(key, data_1, data_2):
    if key in data_1:
        if not data_2.get(key):
            return f'  - {key}: {make_right(data_1.get(key))}\n'
        elif data_2.get(key) == data_1.get(key):
            return f'    {key}: {make_right(data_1.get(key))}\n'
        elif data_2.get(key) != data_1.get(key):
            return f'  - {key}: {make_right(data_1.get(key))}\n'\
                   f'  + {key}: {make_right(data_2.get(key))}\n'
    elif key in data_2:
        return f'  + {key}: {make_right(data_2.get(key))}\n'


def generate_diff(filepath_1, filepath_2):
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
            set_keys = {key for key in chain(data_1.keys(), data_2.keys())}
            sorted_keys = sorted(set_keys)
            result = '{\n'
            for key in sorted_keys:
                result += get_string(key, data_1, data_2)
    return result + '}'
