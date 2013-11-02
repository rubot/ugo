BASE_ARGS = """
    "-v": {
        "argparse_argument_args": "'--verbose', action='count'"
    }
"""

BASE_COMMANDS = """
    "use": {
        "arguments": {
            "commandset": {
                "options": {
                    "call": "utils.get_commandsets"
                },
                "argparse_argument_args": "nargs='?'"
            },
            "virtualenv": {
                "options": {
                    "call": "utils.get_commandsets"
                },
                "argparse_argument_args": "nargs='?'"
            },
            "gemset": {
                "options": {
                    "call": "utils.get_commandsets"
                },
                "argparse_argument_args": "nargs='?'"
            }
        }
    }"""
