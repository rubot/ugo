COMMAND_SET_DESCRIPTION = 'Commandline bookmarks from hell 2.'
COMMANDS = """
    "example": {
        "arguments": {
            "list": {
                "substitutes": {
                    "list": "gu,fa, fub"
                }

            },
            "call": {
                "substitutes": {
                    "call": "utils.get_projects"
                }
            },
            "path_settings": {
                "substitutes": {
                    "path": "BOOTSCRIPT_PATH"
                }
            },
            "path_system": {
                "substitutes": {
                    "path": "/Users/rubot/.ugo"
                }
            },
            "--opts": {
                "options": {
                    "call": "utils.get_pathlist"
                }
            }
        }

    }"""
