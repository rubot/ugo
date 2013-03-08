import subprocess

from settings import BOOTSCRIPT_PATH
from lib.utils import list_files


# Executes script
def ugo_switch(f):
    print f
    if not f.file:
        list_files(BOOTSCRIPT_PATH)
    else:
        script = "%s/%s" % (BOOTSCRIPT_PATH, f.file)
        if f.verbose > 0:
            print 'Executing %s' % script
        subprocess.call(script, shell=True)
