import yaml
import json
from gendiff.differences import make_diff, get_keys, get_status, get_value
from yaml.loader import SafeLoader


INDENTATION_LEVEL = 4
OFFSET_LEFT = 2


def make_correctly(data, depth):
    if isinstance(data, bool):
        return ' true\n' if data else ' false\n'
    elif isinstance(data, dict):
        indent = (depth + 1) * INDENTATION_LEVEL
        result = ' {\n'
        for key in sorted(data.keys()):
            value = data[key]
            if not isinstance(value, dict):
                result += f'{indent * " "}{key}: {value}\n'
            else:
                result += f'{indent * " "}{key}:'
                result += make_correctly(value, depth + 1)
        return result + f'{depth * INDENTATION_LEVEL * " "}{"}"}\n'
    elif data == '':
        return '\n'
    return f' {data}\n' if data is not None else ' null\n'


def stylish(diff): # noqa C901

    def walk(diff, depth):
        keys = get_keys(diff)
        result = ''
        count_space = depth * INDENTATION_LEVEL - OFFSET_LEFT
        indent = count_space * " "
        for key in keys:
            status = get_status(diff, key)
            if status == 'correct':
                value = get_value(diff, key)
                result += f'{indent}  {key}:{make_correctly(value, depth)}'
            elif status == 'changed':
                old_value, new_value = get_value(diff, key)
                result += f'{indent}- {key}:{make_correctly(old_value, depth)}'
                result += f'{indent}+ {key}:{make_correctly(new_value, depth)}'
            elif status == 'deleted':
                value = get_value(diff, key)
                result += f'{indent}- {key}:{make_correctly(value, depth)}'
            elif status == 'added':
                value = get_value(diff, key)
                result += f'{indent}+ {key}:{make_correctly(value, depth)}'
            elif status == 'node':
                child = get_value(diff, key)
                result += f'{indent}  {key}: {"{"}\n'
                result += walk(child, depth + 1)
        return result + ('}' if depth == 1
                         else f'{(count_space - 2) * " "}{"}"}\n')

    return '{\n' + walk(diff, 1)


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
