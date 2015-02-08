from optparse import OptionParser
import os
from django.contrib.auth.models import User
from cms.models import File
from .base import *
from .exceptions import *


class chown(baseplugin):

    def __init__(self):
        super(chown, self).__init__()
        parser = OptionParser()
        self.parser = parser

    def process(self, environ, args):
        options, args = self.parser.parse_args(args)
        if len(args) < 2:
            raise MissArguments()
        try:
            user = User.objects.get(username=args[0])
        except Exception:
            raise UserNotFound(args[0])
        args.pop(0)
        not_success = []
        for i in args:
            path = os.path.join(environ['path'], i)
            path_list = path_str_to_list(path)
            try:
                file = File.objects.get(path=path_list)
            except Exception:
                not_success.append(['FileNotFound', path])
            else:
                if environ['user'].is_superuser or \
                        file.user.username == environ['username']:
                    file.user = user
                    file.save()
                else:
                    not_success.append(['Permission denied:', path])
        if len(not_success) > 0:
            return not_success
        else:
            return None


process_object = chown()
process = process_object.process
