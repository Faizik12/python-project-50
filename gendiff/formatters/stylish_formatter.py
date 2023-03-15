INDENTATION_LEVEL = 4
OFFSET_LEFT = 2


def get_status(diff, key):
    if 'children' in diff['children'][key]:
        return 'node'
    value_1 = diff['children'][key]['old_value']
    value_2 = diff['children'][key]['new_value']
    if value_1 == '|Empty|':
        status = 'added'
    elif value_2 == '|Empty|':
        status = 'deleted'
    elif value_1 == value_2:
        status = 'correct'
    elif value_1 != value_2:
        status = 'changed'
    return status


def get_keys(diff):
    return diff['sorted_keys']


def get_value(diff, key):
    if get_status(diff, key) == 'node':
        return diff['children'][key]
    else:
        return (diff['children'][key]['old_value'],
                diff['children'][key]['new_value'])


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


def get_string(status, old_value, new_value, key, indent, depth):
    if status == 'correct':
        return f'{indent}  {key}:{make_correct(old_value, depth)}'
    elif status == 'changed':
        return f'{indent}- {key}:{make_correct(old_value, depth)}'\
               f'{indent}+ {key}:{make_correct(new_value, depth)}'
    elif status == 'deleted':
        return f'{indent}- {key}:{make_correct(old_value, depth)}'
    elif status == 'added':
        return f'{indent}+ {key}:{make_correct(new_value, depth)}'


def stylish(diff):

    def walk(diff, depth):
        keys = get_keys(diff)
        result = ''
        count_space = depth * INDENTATION_LEVEL - OFFSET_LEFT
        indent = count_space * ' '
        for key in keys:
            status = get_status(diff, key)
            old_value, new_value = get_value(diff, key)
            if status == 'node':
                children = get_value(diff, key)
                result += f'{indent}  {key}: {"{"}\n'
                result += walk(children, depth + 1)
                continue
            result += get_string(status, old_value, new_value,
                                 key, indent, depth)
        return result + ('}' if depth == 1
                         else f'{(count_space - 2) * " "}{"}"}\n')

    return '{\n' + walk(diff, 1)
