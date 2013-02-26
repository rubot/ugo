import os
import sys

import settings
from utils import get_projects

from defined_commands import COMMANDS


def _subs(arguments):
    subslist = []
    for key, value in arguments.items():
        key = str(key)
        if key == "file":
            path = value['path']
            if hasattr(settings, path):
                path = getattr(settings, path)
            subslist = os.listdir(path)

        elif key == "project":
            subslist = get_projects()

        value['subslist'] = subslist
        arguments[key] = value

    return arguments


def _set_subs(_list):

    for pos, value in enumerate(_list):

        if 'subslist' in value[1]:
            i = pos + 1
            _list[i:i] = value[1]['subslist']
            _list.pop(pos)
            break
        else:
            _list[pos] = value[0]

    return _list


def _order_choices(arguments, subcommands):

    choices = []
    unordered_arguments = []
    ordered_arguments = []

    for argument, attributes in arguments.items():
        if 'group' in attributes:
            if attributes['group'] == 'ordered_selection':
                ordered_arguments.append((argument, attributes))
        else:
            unordered_arguments.append((argument, attributes))

    if ordered_arguments:
        unordered_arguments.append(ordered_arguments[0])

    choices.extend(_set_subs(unordered_arguments))
    choices.extend(subcommands.keys())

    return choices


def _get_arguments(clist):
    return clist['arguments'] if 'arguments' in clist else {}


def _get_subcommands(clist):
    return clist['subcommands'] if 'subcommands' in clist else {}


def _find_subs(w, arguments):

    subs = _subs(arguments)
    #print "HOCU:%s" % subs

    for k, v in subs.items():
        if 'subslist' in v:
            if w in v['subslist']:
                del arguments[k]
        else:
            arguments[k] = subs[k]

    return arguments


def _get_current_choices(clist, cwords):

    arguments = _get_arguments(clist)
    subcommands = _get_subcommands(clist)

    for w in cwords:
        if w in arguments:
            del arguments[w]
        elif w in subcommands:
            arguments = _get_arguments(subcommands[w])
            subcommands = _get_subcommands(subcommands[w])
            arguments = _find_subs(w, arguments)
        else:
            arguments = _find_subs(w, arguments)

    return _order_choices(arguments, subcommands)


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
