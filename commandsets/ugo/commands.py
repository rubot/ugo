COMMANDS = """
    "boot": {
        "arguments": {
            "file": {
                "parser_args": "nargs='?'",
                "path": "BOOTSCRIPT_PATH"
                },
            "project": {
                "parser_args": "nargs='?'"
                }
        }
    },
    "conf": {
        "subcommands": {
            "go": {
                "arguments": {
                    "project": {

                    }
                }
            },
            "list": {

            }
        }
    },
    "delete": {
        "arguments": {
            "project": {},
            "--all": {
                "parser_args": "action='store_true'",
                "group": "no_order"
                }
        }
    },
    "go": {
        "arguments": {
            "project": {}
        }
    },
    "help": {

    },
    "info": {
        "arguments": {
            "project": {
                "parser_args": "nargs='?'"
            }
        }
    },
    "list": {
        "arguments": {
            "project": {
                "parser_args": "nargs='?'"
            }
        }
    },
    "make": {
        "arguments": {
            "name": {
                "subslist": {
                    "call": "utils.get_possible_project_names"
                }
            },
            "--path": {}

        }
    },
    "set": {
        "arguments": {
            "project": {},
            "--path": {}
        }
    }"""
