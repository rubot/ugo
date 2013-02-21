COMMANDS = {
    'boot': {
        'file': {
            'args': 'nargs="?"',
            'path': 'BOOTSCRIPT_PATH'
            },
        'project': {
            'args': 'nargs="?"'
            }
    },
    'conf': {
        'project': {
            'args': ''
            }
    },
    'delete': {
        'project': {
            'args': ''
            },
        '--all': {
            'args': 'action="store_true"'
            }
    },
    'go': {
        'project': {
            'args': ''
            }
    },
    'help': {

    },
    'info': {
        'project': {
            'args': 'nargs="?"'
            }
    },
    'list': {
        'project': {
            'args': ''
            }
    },
    'make': {
        'project': {
            'args': ''
            },
        'path': {
            'args': 'nargs="?"'
            }
    },
    'set': {
        'project': {
            'args': ''
            },
        'path': {
            'args': 'nargs="?"'
            }
    }
}
