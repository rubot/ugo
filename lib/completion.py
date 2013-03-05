import os
import sys

import settings

from lib.utils import get_projects, lazy_import, get_commands

COMMANDS = get_commands()


def _check_group(group, attributes):
    return 'group' in attributes and attributes['group'] == group


def _set_subs(_list):

    subslist = []

    for pos, value in enumerate(_list):
        if 'subslist' in value[1]:
            subslist.extend(value[1]['subslist'])
        else:
            subslist.append(value[0])

    return subslist


def _order_choices(arguments, subcommands, last_argument):

    choices = []
    unordered_arguments = []
    ordered_arguments = []

    for argument, attributes in arguments.items():
        if _check_group('no_order', attributes):
            unordered_arguments.append((argument, attributes))
        else:
            ordered_arguments.append((argument, attributes))

    if ordered_arguments:
        ordered_arguments = [ordered_arguments[0]]

        unordered_arguments.extend(ordered_arguments)

    choices.extend(_set_subs(unordered_arguments))
    choices.extend(subcommands.keys())

    return choices


def _get_arguments(clist):
    return clist['arguments'] if 'arguments' in clist else {}


def _get_subcommands(clist):
    return clist['subcommands'] if 'subcommands' in clist else {}


def _subs(arguments):
    subslist = None

    for key, value in arguments.items():
        key = str(key)
        if not 'subslist' in value:
            if key == "file":
                path = value['path']
                if hasattr(settings, path):
                    path = getattr(settings, path)
                subslist = os.listdir(path)

            elif key == "project":
                subslist = get_projects()

        elif isinstance(value['subslist'], dict):
            for k, v in value['subslist'].items():
                if k == "path":
                    if hasattr(settings, v):
                        v = getattr(settings, v)
                    subslist = os.listdir(v)
                elif k == "call":
                    func = lazy_import("%s" % v, 'lib', [''])
                    subslist = func()
                elif k == "list":
                    subslist = v.replace(' ', '').split(',')

        if subslist:
            value['subslist'] = subslist
            arguments[key] = value
            subslist = None

    return arguments


def _find_subs(w, arguments):

    subs = _subs(arguments)
    last_argument = None

    for k, v in subs.items():
        if 'subslist' in v:
            if w in v['subslist']:
                del arguments[k]
                last_argument = k
        # else:
        #     arguments[k] = subs[k]

    return arguments, last_argument


def _get_current_choices(clist, cwords):

    arguments = _get_arguments(clist)
    subcommands = _get_subcommands(clist)
    last_argument = None

    for w in cwords:
        if w in arguments:
            del arguments[w]
        elif w in subcommands:
            arguments = _get_arguments(subcommands[w])
            arguments, last_argument = _find_subs(w, arguments)
            subcommands = _get_subcommands(subcommands[w])
        else:
            arguments, last_argument = _find_subs(w, arguments)

    return _order_choices(arguments, subcommands, last_argument)


def autocomplete():

    if 'COMP_WORDS' in os.environ:

        cwords = os.environ['COMP_WORDS'].split()[1:]

        cword = int(os.environ['COMP_CWORD'])

        try:
            curr = cwords[cword - 1]
        except IndexError:
            curr = ''

        choices = _get_current_choices(COMMANDS, cwords)

        print ' '.join(filter(lambda x: x.startswith(curr), choices))

        sys.exit(1)
