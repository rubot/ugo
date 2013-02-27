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
                    "group": "ordered_selection"
                    },
                "project": {
                    "parser_args": "nargs='?'",
                    "group": "ordered_selection"
                    },
                "zoro": {
                    "parser_args": ""
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
                    "group": "ordered_selection"
                    },
                "--all": {
                    "parser_args": "action='store_true'",
                    "group": "ordered_selection"
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
                    "group": "ordered_selection"
                    },
                "path": {
                    "parser_args": "nargs='?'",
                    "group": "ordered_selection"
                    }
            }
        },
        "set": {
            "arguments": {
                "project": {
                    "parser_args": "",
                    "group": "ordered_selection"
                    },
                "path": {
                    "parser_args": "nargs='?'",
                    "group": "ordered_selection"
                    }
            }
        }
    }
}""", object_pairs_hook=OrderedDict)
