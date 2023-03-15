def make_diff(data_1, data_2):
    all_keys = data_1.keys() | data_2.keys()
    sorted_keys = sorted(all_keys)
    result = {'sorted_keys': sorted_keys,
              'children': {},
              }
    for key in sorted_keys:
        value_1 = data_1.get(key, '|Empty|')
        value_2 = data_2.get(key, '|Empty|')
        if isinstance(value_1, dict) and isinstance(value_2, dict):
            result['children'][key] = make_diff(value_1, value_2)
        else:
            result['children'][key] = {
                'old_value': value_1,
                'new_value': value_2,
            }
    return result
