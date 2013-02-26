import json
from collections import OrderedDict


COMMANDS = json.loads("""
    {
    "arguments": {
        "-v": {
            "parser_args": "'--verbose', action='count'"
        }
    },
    "subcommands": {
        "boot": {
            "arguments": {
                "file": {
                    "parser_args": "nargs='?'",
                    "path": "BOOTSCRIPT_PATH",
                    "group": "ordered_selection",
                    "position": 1
                    },
                "project": {
                    "parser_args": "nargs='?'",
                    "group": "ordered_selection",
                    "position": 2
                    }
            }
        },
        "conf": {
            "subcommands": {
                "go": {
                    "arguments": {
                        "project": {
                            "parser_args": ""
                        }
                }
                    },
                "list": {
                    "arguments": {

                    }
                }
            }
        },
        "delete": {
            "arguments": {
                "project": {
                    "parser_args": "",
                    "group": "ordered_selection",
                    "position": 1
                    },
                "--all": {
                    "parser_args": "action='store_true'",
                    "group": "ordered_selection",
                    "position": 2
                    }
            }
        },
        "go": {
            "arguments": {
                "project": {
                    "parser_args": ""
                    }
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
                "project": {
                    "parser_args": "",
                    "group": "ordered_selection",
                    "position": 1
                    },
                "path": {
                    "parser_args": "nargs='?'",
                    "group": "ordered_selection",
                    "position": 2
                    }
            }
        },
        "set": {
            "arguments": {
                "project": {
                    "parser_args": "",
                    "group": "ordered_selection",
                    "position": 1
                    },
                "path": {
                    "parser_args": "nargs='?'",
                    "group": "ordered_selection",
                    "position": 2
                    }
            }
        }
    }
}""", object_pairs_hook=OrderedDict)
