from optparse import OptionParser
import os
from django.contrib.auth.models import User
from cms.models import Folder, File
from .base import baseplugin
from .exceptions import UserNotFound, MissArguments


class chown(baseplugin):

    def __init__(self):
        super(chown, self).__init__()
        parser = OptionParser()
        self.parser = parser

    def process(self, session, args):
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
            path = os.path.join(session['path'], i)
            if path.endswith("/"):
                path = path[0:-1]
            try:
                folder = Folder.objects.get(path=path+"/")
            except Exception:
                try:
                    file = File.objects.get(path=path)
                except Exception:
                    not_success.append(i)
                else:
                    file.user = user
                    file.save()
            else:
                folder.user = user
                folder.save()
        if len(not_success) > 0:
            not_success.insert(0, "File not found:")
            return [not_success]
        else:
            return None


process_object = chown()
process = process_object.process
