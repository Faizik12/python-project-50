from gendiff.parser import generate_diff
import pytest


@pytest.mark.parametrize(
    'filepath_1',
    ['tests/fixtures/file1.json', 'tests/fixtures/file3.yml'],
)
@pytest.mark.parametrize(
    'filepath_2',
    ['tests/fixtures/file2.json', 'tests/fixtures/file4.yml'],
)
def test_generate_diff_with_simple_file(filepath_1, filepath_2):
    with open('tests/fixtures/simple_result.txt', 'r') as file:
        result = file.read()
    assert generate_diff(filepath_1, filepath_2) == result


@pytest.mark.parametrize(
    'filepath_1',
    ['tests/fixtures/complex_file1.json', 'tests/fixtures/complex_file3.yml'],
)
@pytest.mark.parametrize(
    'filepath_2',
    ['tests/fixtures/complex_file2.json', 'tests/fixtures/complex_file4.yml'],
)
def test_generate_diff_with_complex_file(filepath_1, filepath_2):
    with open('tests/fixtures/complex_result.txt', 'r') as file:
        result = file.read()
    assert generate_diff(filepath_1, filepath_2) == result


def test_generate_diff_with_plain_formate():
    with open('tests/fixtures/plain_result.txt', 'r') as file:
        result = file.read()
    assert generate_diff('tests/fixtures/complex_file1.json',
                         'tests/fixtures/complex_file2.json', 'plain') == result


def test_generate_diff_with_json_formate():
    with open('tests/fixtures/json_result.json', 'r') as file:
        result = file.read()
    assert generate_diff('tests/fixtures/complex_file1.json',
                         'tests/fixtures/complex_file2.json', 'json') == result
