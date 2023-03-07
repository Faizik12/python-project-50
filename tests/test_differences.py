from gendiff.differences import make_diff, get_status, get_keys, get_value
import pytest

@pytest.fixture
def simple_diff():
    return {
            'status': 'node',
            'sorted keys': ['follow', 'host', 'proxy', 'timeout', 'verbose'],
            'children': {
                'follow': {'status': 'deleted', 'correct value': False},
                'host': {'status': 'correct', 'correct value': 'hexlet.io'},
                'proxy': {'status': 'deleted', 'correct value': '123.234.53.22'},
                'timeout': {'status': 'changed', 'old value': 50, 'new value': 20},
                'verbose': {'status': 'added', 'new value': True},
            },
        }


@pytest.fixture
def complex_diff():
    return {
        'status': 'node',
        'sorted keys': ['common', 'group1', 'group2', 'group3'],
        'children': {
            'common': {
                'status': 'node',
                'sorted keys': ['follow', 'setting1', 'setting2', 'setting3', 'setting4', 'setting5', 'setting6'],
                'children': {
                    'follow': {'status': 'added', 'new value': False},
                    'setting1': {'status': 'correct', 'correct value': 'Value 1'},
                    'setting2': {'status': 'deleted', 'correct value': 200},
                    'setting3': {'status': 'changed', 'old value': True, 'new value': None},
                    'setting4': {'status': 'added', 'new value': 'blah blah'},
                    'setting5': {'status': 'added', 'new value': {'key5': 'value5'}},
                    'setting6': {
                        'status': 'node',
                        'sorted keys': ['doge', 'key', 'ops'],
                        'children': {
                            'doge': {
                                'status': 'node',
                                'sorted keys': ['wow'],
                                'children': {
                                    'wow': {'status': 'changed', 'old value': '', 'new value': 'so much'},
                                },
                            },
                            'key': {'status': 'correct', 'correct value': 'value'},
                            'ops': {'status': 'added', 'new value': 'vops'},
                        },
                    },
                },
            },
            'group1': {
                'status': 'node',
                'sorted keys': ['baz', 'foo', 'nest'],
                'children': {
                    'baz': {'status': 'changed', 'old value': 'bas', 'new value': 'bars'},
                    'foo': {'status': 'correct', 'correct value': 'bar'},
                    'nest': {'status': 'changed', 'old value': {'key': 'value'}, 'new value': 'str'}
                },
            },
            'group2': {'status': 'deleted', 'correct value': {'abc': 12345, 'deep': {'id': 45}}},
            'group3': {'status': 'added', 'new value': {'deep': {'id': {'number': 45}}, 'fee': 100500}}
        },
    }


def test_make_diff_with_flat_object(simple_diff):
    data_1 = {
        'host': 'hexlet.io',
        'timeout': 50, 'proxy':
        '123.234.53.22',
        'follow': False,
    }
    data_2 = {
        'timeout': 20,
        'verbose': True,
        'host': 'hexlet.io',
    }
    assert make_diff(data_1, data_2) == simple_diff


def test_make_diff_with_complex_object(complex_diff):
    data_1 = {
        'common': {
            'setting1': 'Value 1',
            'setting2': 200,
            'setting3': True,
            'setting6': {
                'key': 'value',
                'doge': {
                    'wow': '',
                },
            },
        },
        'group1': {
            'baz': 'bas',
            'foo': 'bar',
            'nest': {
                'key': 'value',
            },
        },
        'group2': {
            'abc': 12345,
            'deep': {
                'id': 45,
            },
        },
    }
    data_2 = {
        'common': {
            'follow': False,
            'setting1': 'Value 1',
            'setting3': None,
            'setting4': 'blah blah',
            'setting5': {
                'key5': 'value5',
            },
            'setting6': {
                'key': 'value',
                'ops': 'vops',
                'doge': {
                    'wow': 'so much',
                },
            },
        },
        'group1': {
            'foo': 'bar',
            'baz': 'bars',
            'nest': 'str'
        },
        'group3': {
            'deep': {
                'id': {
                    'number': 45
                },
            },
            'fee': 100500,
        },
    }
    assert make_diff(data_1, data_2) == complex_diff


def test_get_status(simple_diff, complex_diff):
    assert get_status(simple_diff, 'host') == 'correct'
    assert get_status(simple_diff, 'timeout') == 'changed'
    assert get_status(simple_diff, 'follow') == 'deleted'
    assert get_status(simple_diff, 'verbose') == 'added'
    assert get_status(complex_diff, 'common') == 'node'


def test_get_keys(simple_diff):
    assert get_keys(simple_diff) == ['follow', 'host', 'proxy', 'timeout', 'verbose']


def test_get_value(simple_diff, complex_diff):
    assert get_value(simple_diff, 'host') == 'hexlet.io'
    assert get_value(simple_diff, 'timeout') == (50, 20)
    assert get_value(simple_diff, 'follow') == False
    assert get_value(simple_diff, 'verbose') == True
    assert get_value(complex_diff, 'group1') == {
                'status': 'node',
                'sorted keys': ['baz', 'foo', 'nest'],
                'children': {
                    'baz': {'status': 'changed', 'old value': 'bas', 'new value': 'bars'},
                    'foo': {'status': 'correct', 'correct value': 'bar'},
                    'nest': {'status': 'changed', 'old value': {'key': 'value'}, 'new value': 'str'}
                },
            }
