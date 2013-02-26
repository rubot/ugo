import argparse

from defined_commands import COMMANDS
from utils import lazy_import


def _add_subcommands(cdict, parent, parser):

    for _type in cdict:
        if _type == 'arguments':
            for arg in list(cdict[_type]):
                eval("parser.add_argument('%s', %s)" %
                    (arg, cdict[_type][arg]['parser_args']))

        elif _type == 'subcommands':

            subcommands = {}
            sname = parent if parent else 'main'
            subparsers = parser.add_subparsers(title='%s subcommands' % sname, dest='%s_command' % sname)

            for sub in sorted(cdict[_type]):
                mname = parent if parent else sub
                subcommands[sub] = subparsers.add_parser(sub)

                func = lazy_import("ugo_%s.ugo_%s" % (mname, sub), 'lib.commands', ['commands'])
                subcommands[sub].set_defaults(func=func)
                _add_subcommands(cdict[_type][sub], mname, subcommands[sub])


def execute_from_command_line():

    parser = argparse.ArgumentParser(description='Commandline bookmarks.')

    _add_subcommands(COMMANDS, None, parser)

    args = parser.parse_args()
    args.func(args)
