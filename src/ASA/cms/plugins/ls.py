from .base import *
from ..models import *
from .exceptions import *
import os


class ls(baseplugin):

    @staticmethod
    def process(environ, args):
        if len(args) == 0:
            args.append('')
        if isinstance(args[0], str) is False:
            raise WrongArgument(1)
        if access(environ, args[0], AUTH_FOR_READ) is False:
            raise PermissionDenied(os.path.join(envrion['path'], args[0]))
        path_list = path_str_to_list(os.path.join(environ['path'], args[0]))
        return [list(
            map(
                lambda msg: path_list_to_str(msg.path),
                File.objects.filter(parent_folder__path=path_list)
            )
        )]
