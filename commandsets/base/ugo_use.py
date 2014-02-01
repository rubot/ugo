import ConfigParser

from commandsets.base.utils import write_config


def ugo_use(args):
    print args
    args = vars(args)
    _set = args['set']
    _name = args['name']

    if _set == 'commandset':
        ugo_commandset(_name)


def ugo_commandset(name):

    config = ConfigParser.ConfigParser()

    try:
        config.set('SESSION', 'COMMAND_SET', name)
    except ConfigParser.NoSectionError:
        config.add_section('SESSION')
        config.set('SESSION', 'COMMAND_SET', name)

    write_config(config)


def ugo_virtualenv(args):
    print args


def ugo_gemset(args):
    print args
