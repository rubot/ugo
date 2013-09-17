from lib.utils import write_config
import ConfigParser


def ugo_use(args):
    args = vars(args)
    config = ConfigParser.ConfigParser()
    try:
        config.set('SESSION', 'COMMAND_SET', args['set'])
    except ConfigParser.NoSectionError:
        config.add_section('SESSION')
        config.set('SESSION', 'COMMAND_SET', args['set'])

    write_config(config)


def ugo_commandset(args):
    print args


def ugo_virtualenv(args):
    print args


def ugo_gemset(args):
    print args
