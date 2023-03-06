from gendiff.generate_diff import make_right
from gendiff.generate_diff import get_string
from gendiff.generate_diff import generate_diff


def test_make_right():
    assert make_right(True) == 'true'
    assert make_right(False) == 'false'
    assert make_right('Something') == 'Something'
    assert make_right(100) == 100


def test_get_string():
    data_1 = {
        'host': 'hexlet.io',
        'timeout': 50,
        'proxy': '123.234.53.22',
        'follow': False,
        }
    data_2 = {
        'timeout': 20,
        'verbose': True,
        'host': 'hexlet.io',
        }
    assert get_string('follow', data_1, data_2) == f'  - follow: false\n'
    assert get_string('host', data_1, data_2) == f'    host: hexlet.io\n'
    assert get_string('timeout', data_1, data_2) == f'  - timeout: 50\n'\
                                                    f'  + timeout: 20\n'
    assert get_string('verbose', data_1, data_2) == f'  + verbose: true\n'


def test_generate_diff():
    with open('tests/fixtures/simple_result', 'r') as file:
        result = file.read()
    assert generate_diff('tests/fixtures/file1.json',
                         'tests/fixtures/file2.json') == result