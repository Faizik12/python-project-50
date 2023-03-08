from gendiff.differences import get_keys, get_status, get_value


def make_correct(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, dict):
        return '[complex value]'
    elif value is None:
        return 'null'
    elif isinstance(value, str):
        return f"'{value}'"
    return f'{value}'

def plain(diff): # noqa C901

    def walk(diff, path=''):
        keys = get_keys(diff)
        result = ''
        for key in keys:
            current_path = f'{path}.{key}' if path else f'{key}'
            status = get_status(diff, key)
            if status == 'changed':
                old_value, new_value = get_value(diff, key)
                result += f"Property '{current_path}' was updated. From "\
                          f"{make_correct(old_value)} "\
                          f"to {make_correct(new_value)}\n"
            elif status == 'added':
                value = get_value(diff, key)
                result += f"Property '{current_path}' was added with value: "\
                          f"{make_correct(value)}\n"
            elif status == 'deleted':
                value = get_value(diff, key)
                result += f"Property '{current_path}' was removed\n"
            elif status == 'node':
                children = get_value(diff, key)
                result += walk(children, current_path)
        return result

    return walk(diff)[:-1]
