from .base import *
from .exceptions import *
from ..models import *
from optparse import OptionParser
import os


class touch(baseplugin):

    '''
        touch pathname
    '''

    @staticmethod
    def process(environ, args):
        if len(args) == 0:
            raise Missarguments()
        path_list = path_str_to_list(os.path.join(environ['path'], args[0]))
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
            file_ = File.objects.get(path=path_list)
            file_.save()
        return None
