from .base import *
from .exceptions import *
from ..models import *
from optparse import OptionParser


class touch(baseplugin):

    @staticmethod
    def process(environ, args):
        if len(args) == 0:
            raise Missarguments()
        path_list = path_str_to_list(args[0])
        folder_path_list = path_list[:-1]
        if access(environ, folder_path_list, 0o2) is False:
            raise PermissionDenied(path_list_to_str(folder_path_list))
        try:
            parent_folder = File.objects.get(path=folder_path_list)
            File.objects.create(
                mod=parent_folder.mod,
                user=environ['user'],
                parent_folder=parent_folder,
                path=path_list
            )
        except Exception:
            raise FileExists(path_list_to_str(path_list))
        return None
