import pytest

import os

from eph.jpl.parsers import *
from eph.jpl.shortcuts import raw_data_from_req_file


@pytest.fixture
def vectors_req_file(res_dir):
    return os.path.join(res_dir, 'vectors.ini')


@pytest.fixture
def vectors_source(vectors_req_file):
    return raw_data_from_req_file(vectors_req_file)


@pytest.fixture
def observer_req_file(res_dir):
    return os.path.join(res_dir, 'observer.ini')


@pytest.fixture
def observer_source(observer_req_file):
    return raw_data_from_req_file(observer_req_file)


@pytest.fixture
def elements_req_file(res_dir):
    return os.path.join(res_dir, 'elements.ini')


@pytest.fixture
def elements_source(elements_req_file):
    return raw_data_from_req_file(elements_req_file)


def test_parse_vectors(vectors_source):
    e = parse(vectors_source, target=Eph)
    jd, x, y, z, vx, vy, vz, lt, rg, rr = [e[col] for col in ('JDTDB', 'X', 'Y', 'Z', 'VX', 'VY', 'VZ', 'LT', 'RG', 'RR',)]
    d = (x**2+y**2+z**2)**(1/2)
    v = (vx**2+vy**2+vz**2)**(1/2)
    assert jd.unit == u.day
    assert lt.unit == u.s
    assert all([q.unit == u.km for q in (x, y, z, d, rg,)])
    assert all([q.unit == u.km / u.s for q in (vx, vy, vz, v, rr,)])


def test_parse_observer(observer_source):
    e = parse(observer_source, target=Eph)
    assert 'R.A._(ICRF/J2000.0)' in e.keys()
    assert 'DEC_(ICRF/J2000.0)' in e.keys()


def test_parse_elements(elements_source):
    e = parse(elements_source, target=Eph)
    ecc, tp = [e[col] for col in ('EC', 'Tp')]
    assert all(map(lambda x: x < 1, ecc))
    assert tp.unit == u.day
