from lib.utils import list_files, list_projects

from settings import UGO_PATH


def ugo_list(args):
    if not args.project:
        print list_projects()
    else:
        list_files("%s/%s" % (UGO_PATH, args.project))
