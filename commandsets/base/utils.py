import json
import os

import ConfigParser

from collections import OrderedDict

from commandsets.base import settings as base_settings
from commandsets.base import commands


def get_active_commandset(override=None):
    """Get active commandset module path from session file.
    Returns string
    """

    this = get_active_commandset

    if override:
        this.ACTIVE_COMMANDSET = override

    if hasattr(this, 'ACTIVE_COMMANDSET'):
        return 'commandsets.%s' % this.ACTIVE_COMMANDSET

    config = ConfigParser.ConfigParser()

    if config.read(base_settings.CONFIG_FILE):
        CS = config.get('SESSION', 'COMMAND_SET')

        if CS:
            this.ACTIVE_COMMANDSET = CS
            return 'commandsets.%s' % CS

    return 'commandsets.%s' % base_settings.DEFAULT_COMMAND_SET


def get_active_commands_module():
    """Get active commandsets commands module.
    Returns module
    """
    if hasattr(get_active_commands_module, 'commands'):
        return get_active_commands_module.commands
    get_active_commands_module.commands = lazy_import("commands", get_active_commandset(), ['commandsets'])
    return get_active_commands_module.commands


def get_active_commands_description():
    """Get active commandsets description.
    Returns string
    """
    if hasattr(get_active_commands_description, 'description'):
        return get_active_commands_description.description
    c = get_active_commands_module()
    get_active_commands_description.description = c.COMMAND_SET_DESCRIPTION
    return get_active_commands_description.description


def get_active_commands():
    """Get active commandsets commands.
    Returns dict
    """
    if hasattr(get_active_commands, 'commands'):
        return get_active_commands.commands
    c = get_active_commands_module()
    get_active_commands.commands = c.COMMANDS
    return get_active_commands.commands


def get_commands():
    """Return json of all commands. Base and active commandset combined"""
    BASE_ARGS = commands.BASE_ARGS
    BASE_COMMANDS = commands.BASE_COMMANDS

    COMMANDS = get_active_commands()

    DIVIDER = "," if BASE_COMMANDS and COMMANDS else ""
    ALL_COMMANDS = """
{
    "arguments": {
        """ + BASE_ARGS + """
    },
    "subcommands": {
        """ + BASE_COMMANDS + DIVIDER + COMMANDS + """
    }
}"""

    return load_json(ALL_COMMANDS)


def get_setlist():
    """Get all sets for basecommand 'use'.
    Returns list
    """
    cwords, prev, current_word = get_cwords()
    if prev == 'commandset':
        return get_commandsets()
    return ['']


def get_set():
    """Get acitve set for basecommand which set.
    Returns string
    """
    cwords, prev, current_word = get_cwords()
    if prev == 'commandset':
        return get_active_commandset()
    return ''


def get_commandsets():
    """Return listdir of commandsets dir exclude base commandset"""
    commandsets = os.listdir(base_settings.COMMAND_SET_PATH)
    return [c for c in commandsets if not c == "base" and os.path.isdir("%s/%s" % (base_settings.COMMAND_SET_PATH, c))]


#######


def lazy_import(name, module, fromlist, quiet=False):
    """Loads module from module path string."""
    components = name.split('.')
    mod = None
    try:
        mod = __import__('.'.join([module, components[0]]), fromlist=fromlist)

        for comp in components[1:]:
            mod = getattr(mod, comp)
    except ImportError as e:
        if quiet:
            return ''
        print
        print name, "Missing module, or import error.", e, module
        print
    except AttributeError as e:
        if quiet:
            return ''
        print
        print name, "Missing method.", e, module
        print

    return mod


def load_json(commands):
    """Load dict from json.
    Returns OrderedDict
    """
    return json.loads(commands, object_pairs_hook=OrderedDict)


def write_config(config):
    with open(base_settings.CONFIG_FILE, 'wb') as configfile:
        config.write(configfile)


def get_cwords():
    """Get environment completion words.
    Returns cwords, prev, curr.
    """
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


def get_cwd_basename():
    """Get basename of current working directory.
    Returns string
    """
    return get_dir_basename(os.getcwd())


def get_dir_basename(_dir):
    """Return basename of directory"""
    return os.path.basename(_dir)


def get_dir_basepath(_dir):
    """Return basepath of directory"""
    if _dir == "/":
        _dir = ""
    if os.path.exists("%s/" % _dir):
        return os.path.dirname("%s/" % _dir)
    return os.path.dirname(_dir)


def get_files(path):
    return os.listdir(path)


def get_pathlist():
    """Get list of visible directories in path.
    Returns list
    """
    cwords, prev, current_word = get_cwords()
    path = get_dir_basepath(current_word)
    plist = []
    if current_word and os.path.isdir(path):
        if path[-1] != "/":
            path = "%s/" % path
        plist = ["%s%s" % (path, f) for f in get_files(path)]
    else:
        plist = get_files(os.getcwd())
    return [p for p in plist if os.path.isdir(p) and not p.startswith('.')]


def list_files(path):
    for f in get_files(path):
        print f


def shellquote(s):
    if s:
        return s.replace(" ", "_")
    return ""
