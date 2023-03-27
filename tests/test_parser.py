from gendiff.parser import generate_diff
import pytest


@pytest.mark.parametrize(
    'filepath_1,filepath_2,filepath_3,formatter',
    [('tests/fixtures/file1.json', 'tests/fixtures/file2.json',
      'tests/fixtures/simple_result.txt', 'stylish'),
     ('tests/fixtures/file3.yml', 'tests/fixtures/file4.yml',
      'tests/fixtures/simple_result.txt', 'stylish'),
     ('tests/fixtures/complex_file1.json', 'tests/fixtures/complex_file2.json',
      'tests/fixtures/complex_result.txt', 'stylish'),
     ('tests/fixtures/complex_file3.yml', 'tests/fixtures/complex_file4.yml',
      'tests/fixtures/complex_result.txt', 'stylish'),
     ('tests/fixtures/complex_file1.json', 'tests/fixtures/complex_file2.json',
      'tests/fixtures/plain_result.txt', 'plain'),
     ('tests/fixtures/complex_file1.json', 'tests/fixtures/complex_file2.json',
      'tests/fixtures/json_result.json', 'json')])
def test_generate_diff_with_simple_file(filepath_1, filepath_2,
                                        filepath_3, formatter):
    with open(filepath_3, 'r') as file:
        result = file.read()
    assert generate_diff(filepath_1, filepath_2, formatter) == result
