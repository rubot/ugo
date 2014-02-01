import os
import re

from commandsets.base import settings, utils


def get_projects():
    return filter(lambda x: not re.match("^\.", x), utils.get_files(settings.UGO_PATH))


def list_projects():
    for p in get_projects():
        print p


def get_possible_project_names():
    pattern = "^\.|.*\s"
    possible_project_names = [n for n in os.listdir(os.getcwd()) if os.path.isdir(n) and not re.match(pattern, n)]
    possible_project_names.append(utils.get_cwd_basename())
    return possible_project_names
