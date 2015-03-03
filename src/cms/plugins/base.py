from .exceptions import FileNotFound
from ..models import File
import os
from optparse import OptionParser


AUTH_FOR_READ = 4
AUTH_FOR_WRITE = 2
AUTH_FOR_EXECUTE = 1


class basepluginMetaclass(type):

    Register = {}

    def __init__(cls, name, bases, nmspc):
        super(basepluginMetaclass, cls).__init__(name, bases, nmspc)
        basepluginMetaclass.Register[name] = cls


class baseplugin(object, metaclass=basepluginMetaclass):

    parser = OptionParser()

    def __init__(self):
        super(baseplugin, self).__init__()


def path_list_to_str(list_path):
    return '/' + '/'.join(list_path)


def path_str_to_list(str_path):
    list_path = str_path.split('/')
    if list_path[0] == '':
        list_path.pop(0)
    if list_path[-1] == '':
        list_path.pop()
    return list_path


def access(environ, file_, mod):
    if isinstance(file_, str) is True:
        file_ = os.path.join(environ.get('path', ''), file_)
        file_ = path_str_to_list(file_)
    if isinstance(file_, list) is True:
        try:
            file_ = File.objects.get(path=file_)
        except Exception:
            raise FileNotFound(path_list_to_str(file_))
    if isinstance(file_, File):
        if isinstance(mod, int):
            if environ['user'].is_superuser is True:
                return True
            elif file_.user.username == environ['username']:
                return (((file_.mod >> 6) & mod) == mod)
            elif file_.group in file_.groups.all():
                return (((file_.mod >> 3) & mod) == mod)
            else:
                return ((file_.mod & mod) == mod)
        elif isinstance(mod, str):
            if mod == 'host':
                if file_.user.username == environ['username']:
                    return True
                else:
                    return False
    else:
        raise TypeError("Given argument does not relate to any file type")
