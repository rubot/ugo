import os
import sys

import settings

from lib.utils import get_projects, lazy_import, get_commands

COMMANDS = get_commands()


def _check_group(group, attributes):
    return 'group' in attributes and attributes['group'] == group


def _set_subs(argument_list, previous_word):

    subslist = []

    for pos, value in enumerate(argument_list):

        current_argument, current_attributes = value
        previous_argument, previous_attributes = None, None
        if 'previous_argument' in current_attributes:
            previous_argument, previous_attributes = current_attributes['previous_argument']

        if previous_argument:
            if previous_argument == previous_word:
                if 'optslist' in previous_attributes:
                    subslist.extend(previous_attributes['optslist'])
            elif 'subslist' in value[1]:
                subslist.extend(value[1]['subslist'])
            else:
                subslist.append(value[0])
        elif 'subslist' in value[1]:
            subslist.extend(value[1]['subslist'])
        else:
            subslist.append(value[0])

    return subslist


def _order_choices(subcommands, arguments, previous_word):

    choices = []
    unordered_arguments = []
    ordered_arguments = []
    previous_argument = None
    if 'previous_argument' in arguments:
        previous_argument = arguments['previous_argument']
        del arguments['previous_argument']

    for argument, attributes in arguments.items():
        if _check_group('no_order', attributes):
            unordered_arguments.append((argument, attributes))
        else:
            ordered_arguments.append((argument, attributes))

    if ordered_arguments:
        unordered_arguments.extend([ordered_arguments[0]])

    if previous_argument:
        for a in unordered_arguments:
            a[1]['previous_argument'] = previous_argument

    choices.extend(_set_subs(unordered_arguments, previous_word))
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


def _opts(w, arguments):
    optslist = None

    for key, value in arguments.items():
        key = str(key)
        if not 'optslist' in value:
            if key == "--path":
                optslist = ['opa1', 'opu2']
        elif isinstance(value['optslist'], dict):
            for k, v in value['optslist'].items():
                pass

        if optslist:
            value['optslist'] = optslist
            arguments[key] = value
            optslist = None

    return arguments


def _find_subs_and_opts(w, arguments):

    arguments = _subs(arguments)

    # If current word in subslist, delete argument
    for k, v in arguments.items():
        if 'subslist' in v:
            if w in v['subslist']:
                del arguments[k]

    return _opts(w, arguments)


def _get_current_choices(clist, cwords, previous_word):

    arguments = _get_arguments(clist)
    subcommands = _get_subcommands(clist)

    for w in cwords:
        if w in arguments:
            arguments['previous_argument'] = (w, arguments[w])
            del arguments[w]
        elif w in subcommands:
            arguments = _get_arguments(subcommands[w])
            arguments = _find_subs_and_opts(w, arguments)
            subcommands = _get_subcommands(subcommands[w])
        else:
            arguments = _find_subs_and_opts(w, arguments)

    return _order_choices(subcommands, arguments, previous_word)


def autocomplete():

    if 'COMP_WORDS' in os.environ:

        cwords = os.environ['COMP_WORDS'].split()[1:]

        cword = int(os.environ['COMP_CWORD'])

        try:
            curr = cwords[cword - 1]
        except IndexError:
            curr = ''

        try:
            prev = cwords[cword - 2]
        except IndexError:
            prev = ''

        choices = _get_current_choices(COMMANDS, cwords, prev)

        print ' '.join(filter(lambda x: x.startswith(curr), choices))

        sys.exit(1)
