from gendiff.plain_formatter import make_correct, plain
from tests.test_differences import complex_diff # noqa F401


def test_make_correct():
    assert make_correct(False) == 'false'
    assert make_correct(True) == 'true'
    assert make_correct({'key': 'value'}) == '[complex value]'
    assert make_correct(None) == 'null'
    assert make_correct('') == "''"
    assert make_correct('key') == "'key'"
    assert make_correct(45) == '45'


def test_plain_with_complex_diff(complex_diff): # noqa F811
    with open('tests/fixtures/plain_result.txt', 'r') as file:
        result = file.read()
    assert plain(complex_diff) == result
