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
            "no_order": {
                "group": "no_order"
            }
        }
    },
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
