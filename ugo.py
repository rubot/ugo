#! /usr/bin/env python

import os

if os.environ['COMP_WORDS']:
    cwords = os.environ['COMP_WORDS'].split()[1:]

    cword = int(os.environ['COMP_CWORD'])

    try:
        curr = cwords[cword - 1]
    except IndexError:
        curr = ''

    subcommands = ["helo",  "felo", "selo"] + ['help']

    if cword == 1:
        print ' '.join(sorted(filter(lambda x: x.startswith(curr), subcommands)))
