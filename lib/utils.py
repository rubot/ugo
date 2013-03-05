import os
import re

import settings


def get_commands():
    return lazy_import("commands.COMMANDS", settings.COMMAND_SET, ['commandsets'])


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
