import os

from lib.utils import get_cwd_basename


def ugo_make(args):
    print args
    path = args.path or args.name
    print path
    if os.path.isdir(path):
        print "isdir"
        # cd dir. Make project
    else:
        if path == get_cwd_basename():
            print "mydir"
            # Make project
        else:
            print "nopedir"
            # mkdir. Make project

