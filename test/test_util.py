import pytest

from eph.util import *


@pytest.fixture(params=[
    ([1, 2, 3], True),
    ([], True),
    ('abc', False),
    (0, False),
])
def is_vector_data(request):
    return request.param


def test_is_vector(is_vector_data):
    data, result = is_vector_data
    assert is_vector(data) == result


@pytest.fixture(params=[
    (['a ', ' 1'], ['a', '1'])
])
def clean_row_data(request):
    return request.param


def test_clean_row(clean_row_data):
    data, result = clean_row_data
    assert clean_row(data) == result


@pytest.fixture(params=[
    ('a, 1,', ['a', '1']),
])
def parse_row_data(request):
    return request.param


def test_parse_row(parse_row_data):
    data, result = parse_row_data
    assert parse_row(data) == result


@pytest.fixture(params=[
    ('a, 1,\n b , 2,', [['a', '1'], ['b', '2']]),
    ('a, 1,', [['a', '1']]),
])
def parse_table_data(request):
    return request.param


def test_parse_table(parse_table_data):
    data, result = parse_table_data
    assert parse_table(data, rows_del='\n') == result


@pytest.fixture(params=[
    ('1', 1),
    ([], []),
    ([0, 1], [0., 1.]),
    (['a', 'b'], ['a', 'b']),
    ([['a', '1'], ['b', '2']], [['a', 1.], ['b', 2.]]),
])
def numberify_data(request):
    return request.param


def test_numberify(numberify_data):
    data, result = numberify_data
    assert numberify(data) == result


@pytest.fixture(params=[
    ([['a', 'b'], ['1', '2']], [['a', '1'], ['b', '2']]),
])
def transpose_data(request):
    return request.param


def test_transpose(transpose_data):
    data, result = transpose_data
    assert transpose(data) == result


@pytest.fixture(params=[
    ('http://xyz.com', {'key': 'value'}, 'http://xyz.com?key=value'),
    ('http://xyz.com?', {'key': 'value'}, 'http://xyz.com?key=value'),
    ('http://xyz.com?a=b', {'key': 'value'}, 'http://xyz.com?a=b&key=value'),
])
def addparams2url_data(request):
    return request.param


def test_addparams2url(addparams2url_data):
    url, data, result = addparams2url_data
    assert addparams2url(url, data) == result


@pytest.fixture(params=[
    ('abc', '\'abc\''),
    ('\'abc\'', '\'abc\''),
    ('"abc"', '\'abc\''),
])
def wrap_data(request):
    return request.param


def test_wrap(wrap_data):
    s, result = wrap_data
    assert wrap(s) == result


@pytest.fixture(params=[
    ('y', True),
    ('Y', True),
    ('Yes', True),
    (True, True),
    (1, True),
    ('n', False),
    (False, False),
    ('false', False),
    ('bla', None),
])
def yes_or_no_data(request):
    return request.param


def test_yes_or_no(yes_or_no_data):
    value, result = yes_or_no_data
    assert yes_or_no(value, yes=True, no=False) == result
