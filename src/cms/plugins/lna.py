from .base import *
from .exceptions import *
from ..models import *
from django.contrib.contenttypes.models import ContentType


class lna(baseplugin):

    '''
        lna app_label.model id filename
    '''

    @staticmethod
    def process(environ, args):
        if len(args) < 3:
            raise Missarguments()
        app_label, model = args[0].split('.')
        attrib_type = ContentType.objects.get(
            app_label=app_label,
            model=model
        ).model_class()
        attrib = attrib_type.objects.get(id=int(args[1]))
        if access(environ, args[2], 0o2) is True:
            file_ = File.objects.get(path=path_str_to_list(args[2]))
        else:
            raise PermissionDenied(args[2])
        attrib.base_file = file_
        attrib.save()
        return None
