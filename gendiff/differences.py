def make_diff(data_1, data_2): # noqa C901
    all_keys = data_1.keys() | data_2.keys()
    sorted_keys = sorted(all_keys)
    result = {'status': 'node',
              'sorted keys': sorted_keys,
              'children': {}}
    for key in sorted_keys:
        if key in data_1:
            value_1 = data_1.get(key)
            value_2 = data_2.get(key)
            if isinstance(value_1, dict) and isinstance(value_2, dict):
                result['children'][key] = make_diff(value_1, value_2)
            elif key not in data_2:
                result['children'][key] = {
                    'status': 'deleted',
                    'correct value': value_1,
                }
            elif value_1 == value_2:
                result['children'][key] = {
                    'status': 'correct',
                    'correct value': value_1,
                }
            elif value_1 != value_2:
                result['children'][key] = {
                    'status': 'changed',
                    'old value': value_1,
                    'new value': value_2,
                }
        elif key in data_2:
            result['children'][key] = {
                'status': 'added',
                'new value': data_2.get(key)
            }
    return result


def get_status(diff, key):
    return diff['children'][key]['status']


def get_keys(diff):
    return diff['sorted keys']


def get_value(diff, key):
    if get_status(diff, key) == 'correct':
        return diff['children'][key]['correct value']
    elif get_status(diff, key) == 'changed':
        return (diff['children'][key]['old value'],
                diff['children'][key]['new value'])
    elif get_status(diff, key) == 'added':
        return diff['children'][key]['new value']
    elif get_status(diff, key) == 'deleted':
        return diff['children'][key]['correct value']
    elif get_status(diff, key) == 'node':
        return diff['children'][key]
