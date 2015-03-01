from .base import *
from ..models import *
from .exceptions import *
from optparse import OptionParser
import os


class ls(baseplugin):

    parser = OptionParser()

    parser.add_option("-R", "--recursive", dest="recursive",
                      help="list all files in this file",
                      action="store_true", default=False)

    parser.add_option("-r", "--reverse", dest="reverse",
                      help="list files reversely",
                      action="store_true", default=False)

    parser.add_option("--sort", dest="sort",
                      action="append",
                      help="specify list files attrib")

    parser.add_option("-l", dest="line",
                      action="store_true",
                      help="display only one file per line")

    parser.add_option("--op", dest="op",
                      help="specify the serial number for the \
                      first listed file", type="int")

    parser.add_option("--ed", dest="ed",
                      help="specify the serial number for the \
                      last listed file", type="int")

    parser.add_option("--display", dest="display",
                      action="append",
                      help="display attrib of file")

    @staticmethod
    def process(environ, args):
        options, args = ls.parser.parse_args(args)
        if len(args) == 0:
            args.append('')

        # --recursive need admin permission
        if options.recursive is True:
            if environ['user'].is_superuser is False:
                raise PermissionDenied('-R/--recursive is a superuser option')

        # check path permission
        if access(environ, args[0], AUTH_FOR_READ) is False:
            raise PermissionDenied(os.path.join(envrion['path'], args[0]))

        # full path
        path_str = os.path.join(environ['path'], args[0])
        path_list = path_str_to_list(path_str)

        # recursive or not
        if options.recursive is True:
            query_set = File.objects.filter(path__startswith=str(path_list)[:-1] + ',')
        else:
            query_set = File.objects.filter(parent_folder__path=path_list)

        # sort
        if options.sort is not None:
            query_set = query_set.order_by(*options.sort)

        # reverse or not
        if options.reverse is True:
            query_set = query_set.reverse()

        # op & ed
        if options.op is not None and options.ed is not None:
            result = query_set[options.op: options.ed + 1]
        else:
            result = list(query_set)

        # -l line
        if options.line is not None:
            result = [[ele] for ele in result]
            # --display
            for ele in result:
                if options.display is not None:
                    for attrib in options.display:
                        attrib_list = attrib.split("__")
                        dis = ele[0]
                        for sub_attrib in attrib_list:
                            dis = getattr(dis, sub_attrib)
                        ele.append(dis)
                ele[0] = path_list_to_str(ele[0].path)
        else:
            result = [[path_list_to_str(ele.path) for ele in result]]
        return result
