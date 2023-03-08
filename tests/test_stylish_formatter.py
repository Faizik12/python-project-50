from gendiff.stylish_formatter import make_correct, stylish
from tests.test_differences import simple_diff, complex_diff # noqa F401


def test_make_correctly():
    assert make_correct(True, 1) == ' true\n'
    assert make_correct(False, 1) == ' false\n'
    assert make_correct('Something', 1) == ' Something\n'
    assert make_correct(100, 1) == ' 100\n'
    assert make_correct('', 1) == ' \n'
    assert make_correct(None, 1) == ' null\n'
    assert make_correct([1, 2, 3], 1) == ' [1, 2, 3]\n'
    str_result1 = ' {\n        key: value\n    }\n'
    str_result2 = ' {\n        deep: {\n            id: 45\n        }\n    }\n'
    assert make_correct({'key': 'value'}, 1) == str_result1
    assert make_correct({'deep': {'id': 45}}, 1) == str_result2


def test_stylish_with_simple_diff(simple_diff): # noqa F811
    with open('tests/fixtures/simple_result.txt', 'r') as file:
        result = file.read()
    assert stylish(simple_diff) == result


def test_stylish_with_complex_diff(complex_diff): # noqa F811
    with open('tests/fixtures/complex_result.txt', 'r') as file:
        result = file.read()
    assert stylish(complex_diff) == result
