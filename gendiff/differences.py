def create_node(data_1, data_2, key):
    if key in data_1:
        value_1 = data_1.get(key)
        value_2 = data_2.get(key)
        if key not in data_2:
            return {
                'status': 'deleted',
                'old_value': value_1,
            }
        elif value_1 == value_2:
            return {
                'status': 'correct',
                'old_value': value_1,
            }
        elif value_1 != value_2:
            return {
                'status': 'changed',
                'old_value': value_1,
                'new_value': value_2,
            }
    elif key in data_2:
        return {
            'status': 'added',
            'new_value': data_2.get(key),
        }


def make_diff(data_1, data_2):
    all_keys = data_1.keys() | data_2.keys()
    sorted_keys = sorted(all_keys)
    result = {'status': 'node',
              'children': {},
              }
    for key in sorted_keys:
        value_1 = data_1.get(key)
        value_2 = data_2.get(key)
        if isinstance(value_1, dict) and isinstance(value_2, dict):
            result['children'][key] = make_diff(value_1, value_2)
        else:
            result['children'][key] = create_node(data_1, data_2, key)
    return result
