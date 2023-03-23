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


def make_correct(value):
    if isinstance(value, bool):
        result = 'true' if value else 'false'
    elif isinstance(value, dict):
        result = '[complex value]'
    elif value is None:
        result = 'null'
    elif isinstance(value, str):
        result = f'\'{value}\''
    else:
        result = f'{value}'
    return result


def get_string(status, diff, key, path):
    if status == 'changed':
        old_value, new_value = get_value(diff, key)
        result = f'Property \'{path}\' was updated. From '\
                 f'{make_correct(old_value)} '\
                 f'to {make_correct(new_value)}\n'
    elif status == 'added':
        new_value = get_value(diff, key)
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
            if status == 'node':
                children = get_value(diff, key)
                result += walk(children, current_path)
                continue
            result += get_string(status, diff, key, current_path)
        return result

    return walk(diff)[:-1]
