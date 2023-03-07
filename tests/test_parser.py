from gendiff.parser import make_correctly, stylish, generate_diff
from tests.test_differences import simple_diff, complex_diff


def test_make_correctly():
    assert make_correctly(True, 1) == ' true\n'
    assert make_correctly(False, 1) == ' false\n'
    assert make_correctly('Something', 1) == ' Something\n'
    assert make_correctly(100, 1) == ' 100\n'
    assert make_correctly('', 1) == '\n'
    assert make_correctly(None, 1) == ' null\n'
    assert make_correctly([1, 2, 3], 1) == ' [1, 2, 3]\n'
    assert make_correctly({'key': 'value'}, 1) == ' {\n        key: value\n    }\n'
    assert make_correctly({'deep': {'id': 45}}, 1) == ' {\n        deep: {\n            id: 45\n        }\n    }\n'


def test_stylish_with_simple_diff(simple_diff):
    with open('tests/fixtures/simple_result.txt', 'r') as file:
        result = file.read()
    assert stylish(simple_diff) == result


def test_stylish_with_complex_diff(complex_diff):
    with open('tests/fixtures/complex_result.txt', 'r') as file:
        result = file.read()
    assert stylish(complex_diff) == result


def test_generate_diff_with_simple_json():
    with open('tests/fixtures/simple_result.txt', 'r') as file:
        result = file.read()
    assert generate_diff('tests/fixtures/file1.json',
                         'tests/fixtures/file2.json') == result


def test_generate_diff_with_yml():
    with open('tests/fixtures/simple_result.txt', 'r') as file:
        result = file.read()
    assert generate_diff('tests/fixtures/file3.yml',
                         'tests/fixtures/file4.yml') == result


def test_generate_diff_with_complex_json():
    with open('tests/fixtures/complex_result.txt', 'r') as file:
        result = file.read()
    assert generate_diff('tests/fixtures/complex_file1.json',
                         'tests/fixtures/complex_file2.json') == result


def test_generate_diff_with_complex_yml():
    with open('tests/fixtures/complex_result.txt', 'r') as file:
        result = file.read()
    assert generate_diff('tests/fixtures/complex_file3.yml',
                         'tests/fixtures/complex_file4.yml') == result