import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
BOOTSCRIPT_PATH = "%s/scripts" % PROJECT_PATH
UGO_PATH = "%s/%s" % (os.getenv('HOME'), '.ugo')
UGO_PROFILE = ".profile"

COMMAND_SET = "commandsets.default"
