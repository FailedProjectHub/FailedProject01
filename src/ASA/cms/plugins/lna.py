from .base import *
from .exceptions import *
from ..models import *
from optparse import OptionParser
from django.contrib.contenttypes.models import ContentType


class lna(baseplugin):

    @staticmethod
    def process(environ, args):
        if len(args) < 3:
            raise Missarguments()
        app_label, model = args[0].splite('.')
        attrib_type = ContentType.objects.get(app_label=app_label, model=model)
        attrib = attrib_type.objects.get(id=int(args[1]))
        access(environ, args[2], 0o2)
        file_ = models.objects.get(path_str_to_list(args[2]))
        attrib.base_file = file_
        return None
