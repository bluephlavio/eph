import pytest

import os
import datetime
import requests

from eph.jpl import *
from eph.jpl.parsers import parse
from eph.jpl.exceptions import JplParserError, JplBadReq


@pytest.fixture
def urls_file(res_dir):
    return os.path.join(res_dir, 'urls.txt')


@pytest.fixture
def urls(urls_file):
    with open(urls_file, 'r') as f:
        return f.readlines()


@pytest.fixture
def jpleph_file(res_dir):
    return os.path.join(res_dir, 'jpleph.txt')


@pytest.fixture
def jpleph(jpleph_file):
    with open(jpleph_file, 'r') as f:
        return f.read()


@pytest.fixture
def query():
    return {
        'COMMAND': '299',
        'START_TIME': '2000-1-1',
        'STOP_TIME': datetime.date.today().strftime('%Y-%m-%d'),
        'STEP': '2',
    }


@pytest.fixture
def jplreq(query):
    return JplReq(query)


@pytest.fixture(params=[
    ('COMMAND', 'COMMAND'),
    ('Command', 'COMMAND'),
    ('target', 'COMMAND'),
    ('OBJECT', 'COMMAND'),
    ('alias', None)
])
def aliasof_data(request):
    return request.param


def test_aliasof(aliasof_data):
    alias, jplparam = aliasof_data
    assert alias_of(alias) == jplparam


@pytest.fixture(params=[
    ('start', 'START_TIME'),
    ('STOP', 'STOP_TIME'),
    ('origin', 'CENTER'),
    ('param', InvalidParameter),
])
def transformkey_data(request):
    return request.param


def test_transformkey(transformkey_data):
    key, jplparam = transformkey_data
    try:
        assert transform_key(key) == jplparam
    except Exception as e:
        assert e.__class__ == InvalidParameter


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
    ('target', 'COMMAND', 'earth', '399'),
    ('Command', 'COMMAND', 'Earth', '399'),
    ('OBJECT', 'COMMAND', '399', '399'),
    ('Origin', 'CENTER', 'earth', '@399'),
])
def transform_data(request):
    return request.param


def test_transform(transform_data):
    key, transformed_key, value, transformed_value = transform_data
    req = JplReq({key: value})
    assert transformed_key in req.keys()
    assert transformed_value in req.values()


def test_url():
    req = JplReq({'COMMAND': '399'})
    assert req.url() == 'http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND=399'


def test_query(config_file, jplreq):
    jplreq.read(config_file)
    res = jplreq.query().http_response
    assert res.status_code == 200


def test_get(urls):
    for url in urls:
        try:
            res = JplRes(requests.get(url))
            eph = res.get_raw()
            assert bool(eph)
        except JplBadReq:
            assert False


def test_parse(jpleph):
    try:
        eph = parse(jpleph)
        assert bool(eph)
    except JplParserError:
        assert False


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
