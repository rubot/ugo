import argparse

from lib.utils import BASE_COMMANDS_DICT, COMMAND_SET, lazy_import, get_commands


def _load_module(mname, sub, path):
    return lazy_import("ugo_%s.ugo_%s" % (mname, sub), path, ['commandsets'])


def _add_subcommands(cdict, parent, parser):

    for _type in cdict:
        if _type == 'arguments':
            for arg in list(cdict[_type]):
                argparse_argument_args = ""
                if 'argparse_argument_args' in cdict[_type][arg]:
                    argparse_argument_args = cdict[_type][arg]['argparse_argument_args']

                eval("parser.add_argument('%s', %s)" % (arg, argparse_argument_args))

        elif _type == 'subcommands':

            subcommands = {}
            sname = parent if parent else 'main'
            subparsers = parser.add_subparsers(title='%s subcommands' % sname, dest='%s_command' % sname)

            for sub in sorted(cdict[_type]):
                mname = parent if parent else sub
                subcommands[sub] = subparsers.add_parser(sub)

                # TODO Make this more obvious.
                bc = [c for c in BASE_COMMANDS_DICT]
                sbc = [BASE_COMMANDS_DICT[s] for s in bc]
                if sub in bc or [sc for sc in sbc if sub in sc]:
                    func = _load_module(mname, sub, 'commandsets.base')
                else:
                    func = _load_module(mname, sub, COMMAND_SET)

                subcommands[sub].set_defaults(func=func)
                _add_subcommands(cdict[_type][sub], mname, subcommands[sub])


def execute_from_command_line():

    parser = argparse.ArgumentParser(description='Commandline bookmarks.')

    _add_subcommands(get_commands(), None, parser)

    args = parser.parse_args()

    args.func(args)
