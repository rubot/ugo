BASE_ARGS = """
    "-v": {
        "parser_args": "'--verbose', action='count'"
    }
"""

BASE_COMMANDS = """
    "use": {
        "subcommands": {
            "commandset": {
                "arguments": {
                    "optslist": {
                        "call": "utils.get_commandsets",
                        "parser_args": "nargs='?'"
                    }
                }
            },
            "virtualenv": {
                "arguments": {
                    "optslist": {
                        "call": "utils.get_commandsets",
                        "parser_args": "nargs='?'"
                    }
                }
            },
            "gemset": {
                "arguments": {
                    "optslist": {
                        "call": "utils.get_commandsets",
                        "parser_args": "nargs='?'"
                    }
                }
            }
        }
    }"""
