#! /usr/bin/env python

import os

from lib import completion, parse_options


if __name__ == "__main__":

    if 'UGO_AUTO_COMPLETE' in os.environ:
        completion.autocomplete()
    parse_options.execute_from_command_line()
