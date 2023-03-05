import json
from itertools import chain


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


def generate_diff(file_1, file_2):
    with open(file_1, 'r') as file_1:
        with open(file_2, 'r') as file_2:
            data_1 = json.load(file_1)
            data_2 = json.load(file_2)
            set_keys = {key for key in chain(data_1.keys(), data_2.keys())}
            sorted_keys = sorted(set_keys)
            result = '{\n'
            for key in sorted_keys:
                result += get_string(key, data_1, data_2)
    return result + '}'
