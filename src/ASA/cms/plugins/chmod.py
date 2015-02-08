from optparse import OptionParser
from cms.models import File
import os
from .base import baseplugin, path_str_to_list
from .exceptions import MissArguments, WrongArgument


class chmod(baseplugin):

    def __init__(self):
        super(chmod, self).__init__()
        parser = OptionParser()
        self.parser = parser

    def process(self, environ, args):
        options, args = self.parser.parse_args(args)
        if len(args) < 2:
            raise MissArguments()
        try:
            mod = int(args[0], 8)
        except Exception:
            raise WrongArgument(0)
        args.pop(0)
        if (0o0 <= mod <= 0o777) is False:
            raise WrongArgument(0)
        not_success = []
        for i in args:
            path = os.path.join(environ['path'], i)
            list_path = path_str_to_list(path)
            try:
                file = File.objects.get(path=list_path)
            except Exception:
                not_success.append(['No such file:', path])
            else:
                if environ['user'].is_superuser \
                        or file.user.username == environ['username']:
                    file.mod = mod
                    file.save()
                else:
                    not_success.append(["Permission denied:", path])

        if len(not_success) > 0:
            return not_success
        else:
            return None


process_object = chmod()
process = process_object.process
