COMMANDS = """
    "example": {
        "arguments": {
            "list": {
                "subslist": {
                    "list": "gu,fa, fub"
                }

            },
            "call": {
                "subslist": {
                    "call": "utils.get_projects"
                }
            },
            "path_settings": {
                "subslist": {
                    "path": "BOOTSCRIPT_PATH"
                }
            },
            "path_system": {
                "subslist": {
                    "path": "/Users/rubot/.ugo"
                }
            },
            "--opts": {
                "optslist": {
                    "call": "utils.get_pathlist"
                }
            },
            "no_order": {
                "group": "no_order"
            }
        }

    }"""
