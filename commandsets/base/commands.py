BASE_ARGS = """
    "-v": {
        "parser_args": "'--verbose', action='count'"
    }
"""

BASE_COMMANDS = """
    "use": {
        "arguments": {
            "commandset": {
                "optslist": {
                    "call": "utils.get_commandsets"
                },
                "group": "no_order"
            },
            "virtualenv": {
                "optslist": {
                    "call": "utils.get_commandsets"
                },
                "group": "no_order"
            },
            "gemset": {
                "optslist": {
                    "call": "utils.get_commandsets"
                },
                "group": "no_order"
            }
        }
    }"""
