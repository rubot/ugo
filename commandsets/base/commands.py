BASE_ARGS = """
    "-v": {
        "argparse_argument_args": "'--verbose', action='count'"
    }
"""


BASE_COMMANDS = """
    "argparse_subparser_args": "help='base commands'",
    "use": {
        "arguments": {
            "set": {
                "list": "commandset,virtualenv,gemset",
                "argparse_argument_args": "help='set a set'"
            },
            "name": {
                "call": "utils.get_setlist"
            }
        },
        "argparse_subcommand_args": "help='choose a set to use'"
    },
    "which": {
        "arguments": {
            "set": {
                "list": "commandset,virtualenv,gemset"
            }
        },
        "argparse_subcommand_args": "help='show which set is in use'"
    }"""
