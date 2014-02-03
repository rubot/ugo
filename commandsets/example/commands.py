COMMAND_SET_DESCRIPTION = 'Commandline bookmarks from hell 2.'
COMMANDS = """
    "example": {
        "arguments": {
            "list": {
                "list": "gu,fa, fub, nargs='?'"
            },
            "door": {
                "list": "1, 2, 3",
                "argparse_argument_args": "type=int, choices=range(1, 4)"
            },
            "path_settings": {
                "path": "BLA"
            },
            "path_system": {
                "list": "7,8,9",
                "argparse_argument_args": "nargs='?'"
            },
            "--order": {
                "list": "10,11,12",
                "groups": "no_order",
                "argparse_argument_args": "type=int, choices=range(10,13)"
            }
        }
    },
    "example2": {
        "subcommands": {
            "gimmepath": {
                "arguments": {
                    "path": {
                        "call": "get_pathlist"
                    }
                }
            }
        }
    }
"""
