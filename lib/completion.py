import os
import sys

import lib.utils as utils
import settings

COMMANDS = utils.get_commands()


def _check_group(group, attributes):
    return 'groups' in attributes and group in attributes['groups'].replace(' ', '').split(',')


def _set_subs(argument_list, previous_word):

    subslist = []

    for pos, value in enumerate(argument_list):

        current_argument, current_attributes = value
        previous_argument, previous_attributes = None, None
        if 'previous_argument' in current_attributes:
            previous_argument, previous_attributes = current_attributes['previous_argument']

        if current_argument == "" or previous_argument and previous_argument == previous_word:
            if previous_attributes and 'optslist' in previous_attributes:
                subslist.extend(previous_attributes['optslist'])
        elif 'subslist' in current_attributes:
            subslist.extend(current_attributes['subslist'])
        else:
            subslist.append(current_argument)

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
        if unordered_arguments:
            for a in unordered_arguments:
                a[1]['previous_argument'] = previous_argument
        else:
            unordered_arguments.append(('', {'previous_argument': previous_argument}))

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
                subslist = utils.get_projects()

        elif isinstance(value['subslist'], dict):
            for k, v in value['subslist'].items():
                if k == "path":
                    if hasattr(settings, v):
                        v = getattr(settings, v)
                    subslist = os.listdir(v)
                elif k == "call":
                    func = utils.lazy_import("%s" % v, 'lib', [''])
                    subslist = func()
                elif k == "list":
                    subslist = v.replace(' ', '').split(',')

        if subslist:
            value['subslist'] = subslist
            arguments[key] = value
            subslist = None

    return arguments


def _opts(current_word, arguments):
    optslist = None

    for key, value in arguments.items():
        key = str(key)
        if not 'optslist' in value:
            if key == "--path":
                optslist = utils.get_pathlist(current_word)
        elif isinstance(value['optslist'], dict):
            for k, v in value['optslist'].items():
                if k == "path":
                    optslist = utils.get_pathlist(current_word)
                elif k == "call":
                    func = utils.lazy_import("%s" % v, 'lib', [''])
                    optslist = func()
                elif k == "list":
                    optslist = v.replace(' ', '').split(',')

        if optslist:
            value['optslist'] = optslist
            arguments[key] = value
            optslist = None

    return arguments


def _filter_subs(arg, _filter):
    if _filter == "by_tag":
        arg["subslist"] = filter(lambda x: x.startswith("r"), arg["subslist"])

    return arg


def _process_subs(arguments, v, k):
    if _check_group('endless', v):
        if "filter" in v:
            arguments[k] = _filter_subs(arguments[k], v["filter"])
    else:
        del arguments[k]

    return arguments


def _find_subs_and_opts(arguments, cword, current_word):

    arguments = _subs(arguments)

    # If current word in subslist, delete or filter argument
    for k, v in arguments.items():
        if 'subslist' in v:
            if cword in v['subslist']:
                arguments = _process_subs(arguments, v, k)

    return _opts(current_word, arguments)


def _get_current_choices(clist, cwords, previous_word, current_word):

    arguments = _get_arguments(clist)
    subcommands = _get_subcommands(clist)

    for w in cwords:
        if w in arguments:
            arguments['previous_argument'] = (w, arguments[w])
            del arguments[w]
        elif w in subcommands:
            arguments = _get_arguments(subcommands[w])
            arguments = _find_subs_and_opts(arguments, w, current_word)
            subcommands = _get_subcommands(subcommands[w])
        else:
            arguments = _find_subs_and_opts(arguments, w, current_word)

    return _order_choices(subcommands, arguments, previous_word)


def autocomplete():

    cwords, prev, curr = utils.get_cwords()

    choices = _get_current_choices(COMMANDS, cwords, prev, curr)

    print ' '.join(filter(lambda x: x.startswith(curr), [utils.shellquote(c) for c in choices]))

    sys.exit(1)
