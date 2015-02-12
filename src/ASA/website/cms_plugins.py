from cms.plugins.base import baseplugin
from optparse import OptionParser
from .exceptions import *


class av(baseplugin):

    parser = OptionParser()

    @staticmethod
    def process(environ, args):
        args, options = parser.parse_args(args)
        if args[0] == 'init':
            av.init(environ, args, options)

    @staticmethod
    def init(environ, args, options):
        path_list = path_str_to_list(args[0])
        folder_path_list = path_list[:-1]
        if access(environ, folder_path_list, 0o2) is False:
            return Unauthorized("Permission Denied: %s" % (args[0],))
