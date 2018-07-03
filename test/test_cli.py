from eph.cli import parser


def test_parser():
    args = parser.parse_args(['299', '--step', '100d'])
    assert args.objs[0] == '299'
    assert args.step == '100d'
