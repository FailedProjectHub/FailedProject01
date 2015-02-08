from optparse import OptionParser
from .base import *
from .exceptions import *
from ..models import File
import os


class rm(baseplugin):

    def __init__(self):
        super(rm, self).__init__()
        parser = OptionParser()
        parser.add_option("-r",
                          action="store_true",
                          default=False,
                          help="recursive call",
                          dest="recursion")
        self.parser = parser

    def delete_a_file(self, environ, file_):
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
            if self.options.recursion is True:
                for i in file_.sub_file.all():
                    self.delete_a_file(environ, i)
            else:
                raise IsADirectory(path_list_to_str(path_list))
        file_.delete()

    def process(self, environ, args):
        options, args = self.parser.parse_args(args)
        self.options = options
        if len(args) == 0:
            raise MissArguments()
        for i in args:
            self.delete_a_file(environ, i)

process_object = rm()
process = process_object.process
