import pytest

from eph.cli import *


def test_parser():
    ns = parse_args(['2007-11-17', '2017-4-22', '299'])
    assert ns.start == '2007-11-17'
    assert ns.stop == '2017-4-22'
    assert ns.object == '299'
    ns = parse_args(['2007-11-17 00:00', '"2017-4-22 00:00"', 'venus'])
    assert ns.start == '2007-11-17 00:00'
    assert ns.stop == '"2017-4-22 00:00"'
    assert ns.object == '299'
    ns = parse_args(['2007-11-17', '2017-4-22', '299', '--step', '100d'])
    assert ns.step == '100d'
