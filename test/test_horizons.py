import pytest

from eph.horizons import *


@pytest.fixture(params=[
    ('earth', '399'),
    ('\'earth\'', '399'),
    ('Earth', '399'),
    ('399', '399'),
    ('\'399\'', '399'),
    ('pluto', 'pluto'),
])
def codify_obj_data(request):
    return request.param


def test_codify_obj(codify_obj_data):
    data, result = codify_obj_data
    assert codify_obj(data) == result


@pytest.fixture(params=[
    ('earth', '@399'),
    ('\'earth\'', '@399'),
    ('\'@earth\'', '@earth'),
    ('399', '@399'),
    ('\'399\'', '@399'),
    ('\'@399\'', '@399'),
])
def codify_site_data(request):
    return request.param


def test_codify_site(codify_site_data):
    data, result = codify_site_data
    assert codify_site(data) == result


@pytest.fixture(params=[
    ('399', 'earth'),
    ('299', 'venus'),
    ('@499', 'mars'),
    ('1@399', '1@399'),
    ('@earth', '@earth'),
])
def humanify_data(request):
    return request.param


def test_humanify(humanify_data):
    data, result = humanify_data
    assert humanify(data) == result


@pytest.fixture(params=[
    '2017-04-22 00:00',
    Time('2017-4-22'),
])
def format_time_data(request):
    return request.param


def test_format_time(format_time_data):
    assert str(format_time(format_time_data)) == '2017-04-22 00:00'


@pytest.fixture(params=[
    ('COMMAND', 'COMMAND'),
    ('Command', 'COMMAND'),
    ('target', 'COMMAND'),
    ('OBJECT', 'COMMAND'),
    ('table-type', 'TABLE_TYPE'),
    ('key', None),
])
def transformkey_data(request):
    return request.param


def test_transformkey(transformkey_data):
    key, jplparam = transformkey_data
    try:
        assert transform_key(key) == jplparam
    except Exception as e:
        assert e.__class__ == JplBadParamError


@pytest.fixture(params=[
    ('COMMAND', 'earth', '399'),
    ('CENTER', '@399', '@399'),
    ('CENTER', '399', '@399'),
])
def transformvalue_data(request):
    return request.param


def test_transformvalue(transformvalue_data):
    key, value, result = transformvalue_data
    assert transform_value(key, value) == result


@pytest.fixture(params=[
    (('target', 'earth'), ('COMMAND', '399')),
    (('Command', 'Earth'), ('COMMAND', '399')),
    (('OBJECT', '399'), ('COMMAND', '399')),
    (('Origin', 'earth'), ('CENTER', '@399')),
    (('key', 'value'), (None, None)),
])
def transform_data(request):
    return request.param


def test_transform(transform_data):
    data, result = transform_data
    key, value = data
    try:
        assert transform(key, value) == result
    except Exception as e:
        assert e.__class__ == JplBadParamError


@pytest.fixture(params=[
    ('START_TIME', True),
    ('object', True),
    ('key', False),
])
def is_jpl_param_data(request):
    return request.param


def test_is_jpl_param(is_jpl_param_data):
    key, result = is_jpl_param_data
    assert is_jpl_param(key) == result
