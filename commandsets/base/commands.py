BASE_ARGS = """
    "-v": {
        "argparse_argument_args": "'--verbose', action='count'"
    },
    "-c": {
        "argparse_argument_args": "'--commandset'"
    }
"""

BASE_COMMANDS = """
    "argparse_subparser_args": "help='base commands'",
    "use": {
        "base_command": "True",
        "arguments": {
            "set": {
                "list": "commandset,virtualenv,gemset",
                "argparse_argument_args": "help='set a set'"
            },
            "name": {
                "call": "get_setlist"
            }
        },
        "argparse_subcommand_args": "help='choose a set to use'"
    },
    "which": {
        "base_command": "True",
        "arguments": {
            "set": {
                "list": "commandset,virtualenv,gemset"
            }
        },
        "argparse_subcommand_args": "help='show which set is in use'"
    }"""
