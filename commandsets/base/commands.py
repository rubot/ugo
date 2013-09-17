BASE_ARGS = """
    "-v": {
        "argparse_argument_args": "'--verbose', action='count'"
    }
"""

BASE_COMMANDS = """
    "use": {
        "subcommands": {
            "commandset": {
                "arguments": {
                    "set": {
                        "substitutes": {
                            "call": "utils.get_commandsets"
                        }
                    }
                }
            },
            "virtualenv": {
                "arguments": {
                    "options": {
                        "call": "utils.get_commandsets",
                        "argparse_argument_args": "nargs='?'"
                    }
                }
            },
            "gemset": {
                "arguments": {
                    "options": {
                        "call": "utils.get_commandsets",
                        "argparse_argument_args": "nargs='?'"
                    }
                }
            }
        }
    }"""
