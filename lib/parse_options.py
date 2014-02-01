import patched_argparse as argparse

from commandsets.base.utils import lazy_import, get_commands, get_active_commandset, get_active_commands_description
from commandsets.base import settings as base_settings


def _load_module(mname, sub, path):
    return lazy_import("ugo_%s.ugo_%s" % (mname, sub), path, ['commandsets'])


def _add_subcommands(cdict, parent, parser):

    for _type in cdict:
        if _type == 'arguments':
            for arg in cdict[_type]:
                argparse_argument_args = ""
                if 'argparse_argument_args' in cdict[_type][arg]:
                    argparse_argument_args = cdict[_type][arg]['argparse_argument_args']

                eval("parser.add_argument('%s', %s)" % (arg, argparse_argument_args))

        elif _type == 'subcommands':

            subcommands = {}

            sname = parent if parent else 'main'

            argparse_subparser_args = ""
            if 'argparse_subparser_args' in cdict[_type]:
                argparse_subparser_args = cdict[_type]['argparse_subparser_args']
            subparser_args = "title='%(sname)s subcommands', dest='%(sname)s_command', %(subparser_args)s" % {
                'sname': sname,
                'subparser_args': argparse_subparser_args
            }

            subparsers = eval("parser.add_subparsers(%s)" % subparser_args)

            # Patched pythons argparse in lib, because of http://bugs.python.org/issue9351
            for sub in sorted(cdict[_type]):
                if sub in ['argparse_subparser_args']:
                    continue
                mname = parent if parent else sub

                argparse_subcommand_args = ""
                if 'argparse_subcommand_args' in cdict[_type][sub]:
                    argparse_subcommand_args = cdict[_type][sub]['argparse_subcommand_args']

                parser_args = "'%s', %s" % (sub, argparse_subcommand_args)

                subcommands[sub] = eval("subparsers.add_parser(%s)" % parser_args)

                if "base_command" in cdict[_type][sub].keys():
                    func = _load_module(mname, sub, 'commandsets.base')
                else:
                    func = _load_module(mname, sub, get_active_commandset())

                subcommands[sub].set_defaults(func=func)

                _add_subcommands(cdict[_type][sub], mname, subcommands[sub])


def execute_from_command_line():

    parser = argparse.ArgumentParser(description='%s' % get_active_commands_description())

    _add_subcommands(get_commands(), None, parser)

    parser_args = parser.parse_args()

    if parser_args.commandset:
        base_settings.COMMANDLINE_COMMAND_SET = parser_args.commandset

    parser_args.func(parser_args)
