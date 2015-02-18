from optparse import OptionParser
from .base import *
from .exceptions import *
from ..models import File
import os


class rm(baseplugin):

    parser = OptionParser()
    parser.add_option(
        "-r",
        action="store_true",
        default=False,
        help="recursive call",
        dest="recursion")

    @staticmethod
    def delete_a_file(environ, file_):
        if isinstance(file_, str) is True:
            path_list = path_str_to_list(os.path.join(environ['path'], file_))
            try:
                file_ = File.objects.get(path=path_list)
            except File.DoesNotExist:
                raise FileNotFound(path_list_to_str(path_list))
        elif isinstance(file_, File) is False:
            raise TypeError
        # auth
        parent_directory = file_.parent_folder
        access(environ, parent_directory, AUTH_FOR_WRITE)
        if hasattr(file_, 'folderattrib') is True:
            if rm.options.recursion is True:
                for i in file_.sub_file.all():
                    rm.delete_a_file(environ, i)
            else:
                raise IsADirectory(path_list_to_str(path_list))
        file_.delete()

    @staticmethod
    def process(environ, args):
        options, args = rm.parser.parse_args(args)
        rm.options = options
        if len(args) == 0:
            raise MissArguments()
        for i in args:
            rm.delete_a_file(environ, i)
