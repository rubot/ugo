import subprocess

from commandsets.base.settings import BOOTSCRIPT_PATH
from commandsets.base.utils import list_files


# Executes script
def ugo_boot(f):
    print f
    if not f.file:
        list_files(BOOTSCRIPT_PATH)
    else:
        script = "%s/%s" % (BOOTSCRIPT_PATH, f.file)
        if f.verbose > 0:
            print 'Executing %s' % script
        subprocess.call(script, shell=True)
