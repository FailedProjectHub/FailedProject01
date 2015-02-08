from ..models import *
from .base import *
from .exceptions import *
import os


class cd(baseplugin):

    def __init__(self):
        super(cd, self).__init__()

    def process(self, environ, args):
        if len(args) == 0:
            raise Missarguments()
        if isinstance(args[0], str) is False:
            raise WrongArgument(1)
        path = os.path.join(environ["path"], args[0])
        path_list = path_str_to_list(path)
        result = File.objects.filter(path=path_list)
        if result.exists() is False:
            raise FileNotFound(path)
        file = result.get()
        if hasattr(file, "folderattrib") is False:
            AttribNotFound(path, "folder")
        else:
            if access(environ, file, AUTH_FOR_READ+AUTH_FOR_EXECUTE):
                environ['path'] = path
                return None
            else:
                raise PermissionDenied(file.path)

process_object = cd()
process = process_object.process
