import os
from os.path import dirname as dn

PROJECT_PATH = os.path.abspath(dn(dn(dn(__file__))))
BOOTSCRIPT_PATH = "%s/scripts" % PROJECT_PATH
COMMAND_SET_PATH = "%s/commandsets" % PROJECT_PATH

UGO_PATH = "%s/%s" % (os.getenv('HOME'), '.ugo')
UGO_PROFILE = ".profile"

CONFIG_FILE = "%s/.session.ini" % UGO_PATH

DEFAULT_COMMAND_SET = "ugo"
