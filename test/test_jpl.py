import pytest

import os
import datetime
import requests
import unittest

from eph.jpl import *
from eph.jpl.parsers import JplParser
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
        'START_TIME': '2017-1-1',
        'STOP_TIME': datetime.date.today().strftime('%Y-%m-%d'),
    }


@pytest.fixture
def jplreq(query):
    return JplReq(query)


def test_url():
    req = JplReq({'key': 'value'})
    assert req.url() == 'http://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&KEY=value'


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
        eph = JplParser().parse(jpleph)
        assert bool(eph)
    except JplParserError:
        assert False


@pytest.fixture(params=[
    ('earth', '399'),
    ('\'earth\'', '399'),
    ('399', '399'),
    ('\'399\'', '399'),
])
def codify_obj_data(request):
    return request.param


def test_codify_obj(codify_obj_data):
    data, result = codify_obj_data
    assert codify_obj(data) == result


@pytest.fixture(params=[
    ('earth', '\'@399\''),
    ('\'earth\'', '\'@399\''),
    ('\'@earth\'', '\'@399\''),
    ('399', '\'@399\''),
    ('\'399\'', '\'@399\''),
    ('\'@399\'', '\'@399\''),
])
def codify_site_data(request):
    return request.param

def test_codify_site(codify_site_data):
    data, result = codify_site_data
    assert codify_site(data) == result


@pytest.fixture(params=[
    ("'399'", 'earth'),
    ('299', 'venus'),
    ("'@499'", 'mars'),
    ('@0', 'sun'),
])
def humanify_data(request):
    return request.param

def test_humanify(humanify_data):
    data, result = humanify_data
    assert humanify(data) == result
