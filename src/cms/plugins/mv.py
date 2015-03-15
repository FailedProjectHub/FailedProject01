import os

from ..models import *
from .exceptions import *
from .base import *


class mv(baseplugin, metaclass=basepluginMetaclass):

    @staticmethod
    def process(environ, args):
        if (len(args) != 2):
            raise WrongArgumentsNum(3)
        origin_path = os.path.join(environ['path'], args[0])
        dest_path = os.path.join(environ['path'], args[1])
        try:
            origin_file = File.objects.get(path=path_str_to_list(origin_path))
        except Exception:
            raise FileNotFound(origin_path)
        dest_dir = dest_path
        try:
            dest_dir_file = File.objects.get(path=path_str_to_list(dest_dir))
            assert hasattr(dest_dir_file, 'folderattrib') is True
        except Exception:
            raise DirectoryNotFound(dest_dir)
        try:
            assert access(environ, origin_file, AUTH_FOR_WRITE) is True
        except Exception:
            raise PermissionDenied(origin_path)
        try:
            assert access(environ, dest_dir_file, AUTH_FOR_WRITE) is True
        except Exception:
            raise PermissionDenied(dest_dir)
        origin_file.path = path_str_to_list(os.path.join(dest_path, origin_file.path[-1]))
        origin_file.parent_folder = dest_dir_file
        origin_file.save()
