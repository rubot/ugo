COMMAND_SET_DESCRIPTION = 'Commandline bookmarks from hell.'
COMMANDS = """
    "boot": {
        "arguments": {
            "file": {
                "substitutes": {
                    "argparse_argument_args": "nargs='?'",
                    "path": "BOOTSCRIPT_PATH"
                }
            },
            "project": {
                "options": {
                    "argparse_argument_args": "nargs='?'"
                }
            }
        }
    },
    "conf": {
        "subcommands": {
            "go": {
                "arguments": {
                    "project": {
                        "argparse_argument_args": "nargs='?'"
                    }
                }
            },
            "list": {
                "argparse_argument_args": "nargs='?'"
            }
        }
    },
    "delete": {
        "arguments": {
            "project": {},
            "--all": {
                "argparse_argument_args": "action='store_true'",
                "groups": "no_order"
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
                "argparse_argument_args": "nargs='?'"
            }
        }
    },
    "list": {
        "arguments": {
            "project": {
                "argparse_argument_args": "nargs='?'"
            }
        }
    },
    "make": {
        "arguments": {
            "name": {
                "substitutes": {
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
    },
    "tag": {
        "arguments": {
            "project": {
                "groups": "endless",
                "filter": "by_tag"
            }
        }
    }
    """
