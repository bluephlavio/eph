from eph.cli import parser


def test_parser():
    args = parser.parse_args(['2007-11-17', '2017-4-22', '299'])
    assert args.start == '2007-11-17'
    assert args.stop == '2017-4-22'
    assert args.object == '299'
    args = parser.parse_args(['2007-11-17 00:00', '"2017-4-22 00:00"', 'venus'])
    assert args.start == '2007-11-17 00:00'
    assert args.stop == '"2017-4-22 00:00"'
    assert args.object == '299'
    args = parser.parse_args(['2007-11-17', '2017-4-22', '299', '--step', '100d'])
    assert args.step == '100d'
