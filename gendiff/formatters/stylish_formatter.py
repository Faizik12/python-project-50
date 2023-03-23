INDENTATION_LEVEL = 4
OFFSET_LEFT = 2


def get_status(diff, key):
    return diff['children'][key]['status']


def get_keys(diff):
    return list(diff['children'])


def get_value(diff, key):
    if get_status(diff, key) == 'correct':
        return diff['children'][key]['old_value']
    elif get_status(diff, key) == 'changed':
        return (diff['children'][key]['old_value'],
                diff['children'][key]['new_value'])
    elif get_status(diff, key) == 'added':
        return diff['children'][key]['new_value']
    elif get_status(diff, key) == 'deleted':
        return diff['children'][key]['old_value']
    elif get_status(diff, key) == 'node':
        return diff['children'][key]


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


def get_string(status, diff, key, indent, depth):
    if status == 'correct':
        old_value = get_value(diff, key)
        return f'{indent}  {key}:{make_correct(old_value, depth)}'
    elif status == 'changed':
        old_value, new_value = get_value(diff, key)
        return f'{indent}- {key}:{make_correct(old_value, depth)}'\
               f'{indent}+ {key}:{make_correct(new_value, depth)}'
    elif status == 'deleted':
        old_value = get_value(diff, key)
        return f'{indent}- {key}:{make_correct(old_value, depth)}'
    elif status == 'added':
        new_value = get_value(diff, key)
        return f'{indent}+ {key}:{make_correct(new_value, depth)}'


def stylish(diff):

    def walk(diff, depth):
        keys = get_keys(diff)
        result = ''
        count_space = depth * INDENTATION_LEVEL - OFFSET_LEFT
        indent = count_space * ' '
        for key in keys:
            status = get_status(diff, key)
            if status == 'node':
                children = get_value(diff, key)
                result += f'{indent}  {key}: {"{"}\n'
                result += walk(children, depth + 1)
                continue
            result += get_string(status, diff, key, indent, depth)
        return result + ('}' if depth == 1
                         else f'{(count_space - 2) * " "}{"}"}\n')

    return '{\n' + walk(diff, 1)
