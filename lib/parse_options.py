import patched_argparse as argparse

from lib.utils import COMMAND_SET, COMMAND_SET_DESCRIPTION, lazy_import, get_commands, SUB_BASE_COMMANDS_LIST, BASE_COMMANDS_LIST


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
                if sub == 'argparse_subparser_args':
                    continue
                mname = parent if parent else sub

                argparse_subcommand_args = ""
                if 'argparse_subcommand_args' in cdict[_type][sub]:
                    argparse_subcommand_args = cdict[_type][sub]['argparse_subcommand_args']

                parser_args = "'%s', %s" % (sub, argparse_subcommand_args)

                subcommands[sub] = eval("subparsers.add_parser(%s)" % parser_args)

                # print sname, mname, sub, [sc for sc in SUB_BASE_COMMANDS_LIST if 'subcommands' in sc and sub in sc['subcommands'].keys()]
                # check for base_commands have subcommands
                if sub in BASE_COMMANDS_LIST or [sc for sc in SUB_BASE_COMMANDS_LIST if _type in sc and sub in sc[_type].keys()]:
                    func = _load_module(mname, sub, 'commandsets.base')
                else:
                    func = _load_module(mname, sub, COMMAND_SET)

                subcommands[sub].set_defaults(func=func)

                _add_subcommands(cdict[_type][sub], mname, subcommands[sub])


def execute_from_command_line():

    parser = argparse.ArgumentParser(description='%s' % COMMAND_SET_DESCRIPTION)

    _add_subcommands(get_commands(), None, parser)

    parser_args = parser.parse_args()

    parser_args.func(parser_args)
