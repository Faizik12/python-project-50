from gendiff.parser import generate_diff


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