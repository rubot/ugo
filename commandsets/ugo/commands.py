COMMAND_SET_DESCRIPTION = 'Commandline bookmarks from hell.'
COMMANDS = """
    "boot": {
        "arguments": {
            "file": {
                "path": "BOOTSCRIPT_PATH"
            },
            "project": {
                "call": "get_projects",
                "argparse_argument_args": "nargs='?'"
            }
        }
    },
    "conf": {
        "subcommands": {
            "go": {
                "arguments": {
                    "project": {
                        "call": "get_projects",
                        "argparse_argument_args": "nargs='?'"
                    }
                }
            },
            "list": {
                "arguments": {
                    "project": {
                        "list": "la,le,lu",
                        "argparse_argument_args": "nargs='?'"
                    }
                }
            }
        }
    },
    "delete": {
        "arguments": {
            "project": {
                "call": "get_projects"
            },
            "--all": {
                "argparse_argument_args": "action='store_true'",
                "groups": "no_order"
                }
        }
    },
    "go": {
        "arguments": {
            "project": {
                "call": "get_projects"
            }
        }
    },
    "help": {
        "argparse_subcommand_args": "help='Show ugo help', description='Show ugo help'"
    },
    "info": {
        "arguments": {
            "project": {
                "call": "get_projects",
                "argparse_argument_args": "nargs='?'"
            }
        }
    },
    "list": {
        "arguments": {
            "project": {
                "call": "get_projects",
                "argparse_argument_args": "nargs='?'"
            }
        }
    },
    "make": {
        "arguments": {
            "name": {
                "call": "get_possible_project_names"
            },
            "--path": {
                "path": "."
            }

        }
    },
    "set": {
        "arguments": {
            "project": {
                "call": "get_projects"
            },
            "--path": {
                "path": "."
            }
        }
    },
    "tag": {
        "arguments": {
            "project": {
                "call": "get_projects",
                "groups": "endless",
                "filter": "by_tag"
            }
        }
    }
    """
