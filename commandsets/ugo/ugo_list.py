from commandsets.base.utils import list_files
from commandsets.base.settings import UGO_PATH
from commandsets.ugo.utils import list_projects


def ugo_list(args):
    if not args.project:
        print list_projects()
    else:
        list_files("%s/%s" % (UGO_PATH, args.project))
