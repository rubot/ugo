import os
import sys

import settings

from defined_commands import COMMANDS

if 'COMP_WORDS' in os.environ:

    cwords = os.environ['COMP_WORDS'].split()[1:]

    cword = int(os.environ['COMP_CWORD'])

    subcommands = COMMANDS.keys()

    try:
        curr = cwords[cword - 1]
    except IndexError:
        curr = ''

    if cword == 1:
        print ' '.join(filter(lambda x: x.startswith(curr), subcommands))
    elif cwords[0] in subcommands:

        subcommands = COMMANDS[cwords[0]].keys()

        for pos, k in enumerate(subcommands):
            if k == "file":
                i = subcommands.pop(pos)
                path = COMMANDS[cwords[0]]['file']['path']
                if hasattr(settings, path):
                    path = getattr(settings, path)
                new_subcommands = os.listdir(path)
                new_subcommands.extend(subcommands)

        if new_subcommands:
            subcommands = new_subcommands

        if cword - 1 > len(subcommands):
            sys.exit(1)

        print ' '.join(filter(lambda x: x.startswith(curr), filter(lambda x: x for x in subcommands)))

    sys.exit(1)
