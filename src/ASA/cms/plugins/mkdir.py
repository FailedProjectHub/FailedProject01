from cms.models import *
from .base import *
from .exceptions import *
from optparse import OptionParser
from django.db import IntegrityError
import os


def set_up_a_folder(environ, filename):
    path_list = path_str_to_list(os.path.join(environ['path'], filename))
    if access(environ, path_list[:-1], AUTH_FOR_WRITE) is False:
        raise PermissionDenied(path_list_to_str(path_list))
    # TODO:umask
    parent_folder = File.objects.get(path=path_list[:-1])
    if hasattr(parent_folder, 'folderattrib') is False:
        raise DirectoryNotFound(path_list_to_str(path_list[:-1]))
    try:
        file = File.objects.create(
            user=environ['user'],
            mod=parent_folder.mod,
            parent_folder=parent_folder,
            path=path_list
        )
    except IntegrityError:
        raise FileExists(path_list_to_str(path_list))
    FolderAttrib.objects.create(base_file=file)


def recursive(environ, filename):
    path_list = path_str_to_list(os.path.join(environ['path'], filename))
    try:
        File.objects.get(path=path_list[:-1])
    except File.DoesNotExist:
        recursive(environ, filename[:filename.rfind('/')])
    set_up_a_folder(environ, filename)


class mkdir(baseplugin):

    def __init__(self):
        super(mkdir, self).__init__()
        parser = OptionParser()
        parser.add_option("-p", action="store_true", default=False, dest="p")
        self.parser = parser

    def process(self, environ, args):
        options, args = self.parser.parse_args(args)
        not_success = []
        for i in args:
            try:
                if options.p is True:
                    recursive(environ, i)
                else:
                    set_up_a_folder(environ, i)
            except Exception as e:
                raise e
                not_success.append([str(e)])
        if len(not_success) > 0:
            return not_success
        else:
            return None


process_object = mkdir()
process = process_object.process
