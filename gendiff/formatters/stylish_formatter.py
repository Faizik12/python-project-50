from gendiff.differences import get_keys, get_status, get_value


INDENTATION_LEVEL = 4
OFFSET_LEFT = 2


def make_correct(data, depth):
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
                result += make_correct(value, depth + 1)
        return result + f'{depth * INDENTATION_LEVEL * " "}{"}"}\n'
    return f' {data}\n' if data is not None else ' null\n'


def stylish(diff): # noqa C901

    def walk(diff, depth):
        keys = get_keys(diff)
        result = ''
        count_space = depth * INDENTATION_LEVEL - OFFSET_LEFT
        indent = count_space * ' '
        for key in keys:
            status = get_status(diff, key)
            if status == 'correct':
                value = get_value(diff, key)
                result += f'{indent}  {key}:{make_correct(value, depth)}'
            elif status == 'changed':
                old_value, new_value = get_value(diff, key)
                result += f'{indent}- {key}:{make_correct(old_value, depth)}'
                result += f'{indent}+ {key}:{make_correct(new_value, depth)}'
            elif status == 'deleted':
                value = get_value(diff, key)
                result += f'{indent}- {key}:{make_correct(value, depth)}'
            elif status == 'added':
                value = get_value(diff, key)
                result += f'{indent}+ {key}:{make_correct(value, depth)}'
            elif status == 'node':
                children = get_value(diff, key)
                result += f'{indent}  {key}: {"{"}\n'
                result += walk(children, depth + 1)
        return result + ('}' if depth == 1
                         else f'{(count_space - 2) * " "}{"}"}\n')

    return '{\n' + walk(diff, 1)
