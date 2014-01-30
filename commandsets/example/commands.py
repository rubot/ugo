COMMAND_SET_DESCRIPTION = 'Commandline bookmarks from hell 2.'
COMMANDS = """
    "example": {
        "arguments": {
            "list": {
                "list": "gu,fa, fub"
            },
            "door": {
                "list": "1, 2, 3",
                "argparse_argument_args": "type=int, choices=range(1, 4)"
            },
            "path_settings": {
                "list": "4,5,6"
            },
            "path_system": {
                "list": "7,8,9"
            },
            "--order": {
                "list": "10,11,12",
                "groups": "no_order"
            }
        }

    }"""
