import os
import sys

from commandsets.base import utils, settings


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


def _order_choices(subcommands, arguments, previous_word, base_command=False):
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

        oa = ordered_arguments if base_command else [ordered_arguments[0]]
        unordered_arguments.extend(oa)

    if previous_argument:
        if unordered_arguments:
            for a in unordered_arguments:
                a[1]['previous_argument'] = previous_argument
        else:
            unordered_arguments.append(('', {'previous_argument': previous_argument}))

    choices.extend(_set_subs(unordered_arguments, previous_word))
    choices.extend(subcommands.keys())

    excludes = ['argparse_subparser_args']
    return [choice for choice in choices if not choice in excludes]


def _get_arguments(clist):
    return clist['arguments'] if 'arguments' in clist else {}


def _get_subcommands(clist):
    return clist['subcommands'] if 'subcommands' in clist else {}


def _go_and_get_it(value, base_command):
    get_it = None

    if base_command:
        _settings = settings
        _utils = utils
    else:
        _settings = utils.get_active_settings_module()
        _utils = utils.get_active_utils_module()

    if "path" in value:
        v = value['path']
        if hasattr(_settings, v):
            v = getattr(_settings, v)
        try:
            get_it = utils.get_pathlist() if v == "." else os.listdir(v)
        except OSError:
            pass

    elif "call" in value:

        v = value['call']
        func = getattr(_utils, v)
        get_it = func()
    elif "list" in value:
        v = value['list']
        get_it = v.replace(' ', '').split(',')

    return get_it


def _subsopts(arguments, base_command):
    subsopts = None

    for key, value in arguments.items():
        # key = str(key)
        subsopts = _go_and_get_it(value, base_command)

        if subsopts:
            _type = 'options' if key.startswith('-') else 'substitutes'
            value[_type] = subsopts
            arguments[key] = value
            subsopts = None

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


def _process_opts(arguments, v, k):
    del arguments[k]
    return arguments


def _find_subs_and_opts(arguments, cword, cwords, base_command=False):

    arguments = _subsopts(arguments, base_command)

    for k, v in arguments.items():
        # If current word in substitutes, delete or filter argument
        if 'substitutes' in v:
            if cword in v['substitutes']:
                arguments = _process_subs(arguments, v, k)

        # If previous word in options and option-flag in cwords, delete or filter argument
        elif 'options' in v:
            if k in cwords:
                index = cwords.index(k)
                if len(cwords) > index + 1 and cwords[index + 1] in v['options']:
                    arguments = _process_opts(arguments, v, k)

    return arguments


def _get_current_choices(clist, cwords, previous_word, current_word):

    arguments = _get_arguments(clist)
    subcommands = _get_subcommands(clist)
    base_command = True

    for w in cwords:
        if w in arguments:
            arguments['previous_argument'] = (w, arguments[w])
            del arguments[w]
        elif w in subcommands:
            arguments = _get_arguments(subcommands[w])
            base_command = True if 'base_command' in subcommands[w] else False
            arguments = _find_subs_and_opts(arguments, w, cwords, base_command)
            subcommands = _get_subcommands(subcommands[w])
        else:
            arguments = _find_subs_and_opts(arguments, w, cwords, base_command)

    return _order_choices(subcommands, arguments, previous_word, base_command)


def autocomplete():

    cwords, prev, curr = utils.get_cwords()

    choices = _get_current_choices(utils.get_commands(), cwords, prev, curr)

    print ' '.join(filter(lambda x: x.startswith(curr), [utils.shellquote(c) for c in choices]))

    sys.exit(1)
