import os
import subprocess

from settings import *


# Executes script
def _boot(f):

    if not f.file:
        list_bootfiles()
    else:
        script = "%s/%s" % (BOOTSCRIPT_PATH, f.file)
        print 'Executing %s' % script
        subprocess.call(script, shell=True)


def list_bootfiles():
    for f in get_files(BOOTSCRIPT_PATH):
        print f


# Get directory listing
def get_files(path):
    return os.listdir(path)


