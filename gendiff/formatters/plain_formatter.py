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


def make_correct(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, dict):
        return '[complex value]'
    elif value is None:
        return 'null'
    elif isinstance(value, str):
        return f'\'{value}\''
    return f'{value}'


def get_string(status, old_value, new_value, path):
    if status == 'changed':
        result = f'Property \'{path}\' was updated. From '\
                 f'{make_correct(old_value)} '\
                 f'to {make_correct(new_value)}\n'
    elif status == 'added':
        result = f'Property \'{path}\' was added with value: '\
                 f'{make_correct(new_value)}\n'
    elif status == 'deleted':
        result = f'Property \'{path}\' was removed\n'
    else:
        result = ''
    return result


def plain(diff):

    def walk(diff, path=''):
        keys = get_keys(diff)
        result = ''
        for key in keys:
            current_path = f'{path}.{key}' if path else f'{key}'
            status = get_status(diff, key)
            old_value, new_value = get_value(diff, key)
            if status == 'node':
                children = get_value(diff, key)
                result += walk(children, current_path)
                continue
            result += get_string(status, old_value, new_value, current_path)
        return result

    return walk(diff)[:-1]
