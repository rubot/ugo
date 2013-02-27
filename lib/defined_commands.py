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
                            "parser_args": ""
                        }
                    }
                },
                "list": {

                }
            }
        },
        "delete": {
            "arguments": {
                "project": {
                    "parser_args": ""
                    },
                "--all": {
                    "parser_args": "action='store_true'",
                    "group": "no_order"
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
                "name": {
                    "parser_args": "",
                    "subslist": {
                        "list": "gu,fa,fub"
                    }
                },
                "--path": {
                    "parser_args": ""
                }
            }
        },
        "set": {
            "arguments": {
                "project": {
                    "parser_args": ""
                },
                "--path": {
                    "parser_args": ""
                }
            }
        }
    }
}""", object_pairs_hook=OrderedDict)
