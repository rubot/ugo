import os
import sys

import lib.utils as utils
import settings


def _check_group(group, attributes):
    return 'groups' in attributes and group in attributes['groups'].replace(' ', '').split(',')


def _set_subs(argument_list, previous_word):

    substitutes = []

    for pos, value in enumerate(argument_list):

        current_argument, current_attributes = value
        previous_argument, previous_attributes = None, None
        if 'previous_argument' in current_attributes:
            previous_argument, previous_attributes = current_attributes['previous_argument']

        if current_argument == "" or previous_argument and previous_argument == previous_word:
            if previous_attributes and 'options' in previous_attributes:
                substitutes.extend(previous_attributes['options'])
        elif 'substitutes' in current_attributes:
            substitutes.extend(current_attributes['substitutes'])
        else:
            substitutes.append(current_argument)

    return substitutes


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
    substitutes = None

    for key, value in arguments.items():
        key = str(key)
        if not 'substitutes' in value:
            if key == "file":
                path = value['path']
                if hasattr(settings, path):
                    path = getattr(settings, path)
                substitutes = os.listdir(path)

            elif key == "project":
                substitutes = utils.get_projects()

        elif isinstance(value['substitutes'], dict):
            for k, v in value['substitutes'].items():
                if k == "path":
                    if hasattr(settings, v):
                        v = getattr(settings, v)
                    substitutes = os.listdir(v)
                elif k == "call":
                    func = utils.lazy_import("%s" % v, 'lib', [''])
                    substitutes = func()
                elif k == "list":
                    substitutes = v.replace(' ', '').split(',')

        if substitutes:
            value['substitutes'] = substitutes
            arguments[key] = value
            substitutes = None

    return arguments


def _opts(current_word, arguments):
    options = None

    for key, value in arguments.items():
        key = str(key)
        if not 'options' in value:
            if key == "--path":
                options = utils.get_pathlist(current_word)
        elif isinstance(value['options'], dict):
            for k, v in value['options'].items():
                if k == "path":
                    options = utils.get_pathlist(current_word)
                elif k == "call":
                    func = utils.lazy_import("%s" % v, 'lib', [''])
                    options = func()
                elif k == "list":
                    options = v.replace(' ', '').split(',')

        if options:
            value['options'] = options
            arguments[key] = value
            options = None

    return arguments


def _filter_subs(arg, _filter):
    if _filter == "by_tag":
        arg["substitutes"] = filter(lambda x: x.startswith("r"), arg["substitutes"])

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

    # If current word in substitutes, delete or filter argument
    for k, v in arguments.items():
        if 'substitutes' in v:
            if cword in v['substitutes']:
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

    choices = _get_current_choices(utils.get_commands(), cwords, prev, curr)

    print ' '.join(filter(lambda x: x.startswith(curr), [utils.shellquote(c) for c in choices]))

    sys.exit(1)
