import json
import os
import re
import sys
from collections import OrderedDict

import settings


def get_cwords():
    if 'COMP_WORDS' in os.environ:
        cwords = os.environ['COMP_WORDS'].split()[1:]

        cword = int(os.environ['COMP_CWORD'])

        try:
            prev = cwords[cword - 2]
        except IndexError:
            prev = ''

        try:
            curr = cwords[cword - 1]
        except IndexError:
            curr = ''

        return cwords, prev, curr
    #sys.exit(1)


def get_pathlist():
    cwords, prev, current_word = get_cwords()
    path = get_dir_basepath(current_word)
    plist = []
    if current_word and os.path.isdir(path):
        if path[-1] != "/":
            path = "%s/" % path
        plist = ["%s%s" % (path, f) for f in get_files(path)]
    else:
        plist = get_files(os.getcwd())
    return [p for p in plist if os.path.isdir(p)]


def get_cwd_basename():
    return get_dir_basename(os.getcwd())


def get_dir_basename(_dir):
    return os.path.basename(_dir)


def get_dir_basepath(_dir):
    if _dir == "/":
        _dir = ""
    if os.path.exists("%s/" % _dir):
        return os.path.dirname("%s/" % _dir)
    return os.path.dirname(_dir)


def get_possible_project_names():
    pattern = "^\.|.*\s"
    possible_project_names = [n for n in os.listdir(os.getcwd()) if os.path.isdir(n) and not re.match(pattern, n)]
    possible_project_names.append(get_cwd_basename())
    return possible_project_names


def get_commandsets():
    commandsets = os.listdir(settings.COMMAND_SET_PATH)
    return [c for c in commandsets if not c == "base" and os.path.isdir("%s/%s" % (settings.COMMAND_SET_PATH, c))]


def get_commands():

    COMMAND_SET = settings.DEFAULT_COMMAND_SET
    COMMANDS = lazy_import("commands.COMMANDS", COMMAND_SET, ['commandsets'])

    try:
        BASE_ARGS = lazy_import("commands.BASE_ARGS", 'commandsets.base', ['commandsets'])
        BASE_COMMANDS = lazy_import("commands.BASE_COMMANDS", 'commandsets.base', ['commandsets'])

    except:
        BASE_ARGS = ""
        BASE_COMMANDS = ""

    DIVIDER = "," if BASE_COMMANDS and COMMANDS else ""
    ALL_COMMANDS = """
{
    "arguments": {
        """+BASE_ARGS+"""
    },
    "subcommands": {
        """+BASE_COMMANDS+DIVIDER+COMMANDS+"""
    }
}"""

    return load_json(ALL_COMMANDS)


def load_json(commands):
    return json.loads(commands, object_pairs_hook=OrderedDict)


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
        print name, "Missing module."
        print

    return mod


def list_files(path):
    for f in get_files(path):
        print f


def list_projects():
    for p in get_projects():
        print p


def shellquote(s):
    if s:
        return s.replace(" ", "_")
    return ""
