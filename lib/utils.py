import json
import os
import re

from collections import OrderedDict

import settings


def get_cwd_basename():
    return os.getcwd().split("/")[-1]


def get_possible_project_names():
    pattern = "^\.|.*\s"
    possible_project_names = [n for n in os.listdir(os.getcwd()) if os.path.isdir(n) and not re.match(pattern, n)]
    possible_project_names.append(get_cwd_basename())
    return possible_project_names


def get_commands():
    COMMANDS = lazy_import("commands.COMMANDS", settings.COMMAND_SET, ['commandsets'])

    return json.loads("""
{
    "arguments": {
        "-v": {
            "parser_args": "'--verbose', action='count'"
        }
    },
    "subcommands": {
        """+COMMANDS+"""
    }
}""", object_pairs_hook=OrderedDict)


def get_files(path):
    return os.listdir(path)


def get_projects():
    return filter(lambda x: not re.match("^\.", x), get_files(settings.UGO_PATH))


def lazy_import(name, module, fromlist):
    components = name.split('.')
    mod = None
    try:
        mod = __import__('.'.join([module, components[0]]), fromlist=fromlist)

        for comp in components[1:]:
            mod = getattr(mod, comp)
    except:
        print
        print name, "Missing subcommand."
        print

    return mod


def list_files(path):
    for f in get_files(path):
        print f


def list_projects():
    for p in get_projects():
        print p
