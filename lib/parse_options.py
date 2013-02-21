import argparse

from defined_commands import COMMANDS


def lazy_import(name):
    components = name.split('.')
    mod = __import__('.'.join(['lib.commands', components[0]]), fromlist=['commands'])

    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def execute_from_command_line():
    parser = argparse.ArgumentParser(description='Commandline bookmarks.')

    parser.add_argument('-v', '--verbose', action='count')

    subparsers = parser.add_subparsers(title='subcommands', dest='command')

    subcommands = {}
    for key in COMMANDS:
        subcommands[key] = subparsers.add_parser(key)
        for arg_name in reversed(list(COMMANDS[key])):
            eval("subcommands['%s'].add_argument('%s',%s)" % (key, arg_name, COMMANDS[key][arg_name]['args']))
        func = lazy_import("_%s._%s" % (key, key))
        subcommands[key].set_defaults(func=func)

    args = parser.parse_args()
    args.func(args)
