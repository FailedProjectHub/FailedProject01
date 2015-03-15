class AttribNotFound(Exception):

    def __init__(self, path, attrib):
        self.path = path
        self.attrib = attrib

    def __str__(self):
        return "File %s has no such attrib: %s" % (self.path, self.attrib)


class FileNotFound(Exception):

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "no such file: %s" % (self.path,)


class DirectoryNotFound(Exception):

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "no such directory: %s" % (self.path,)


class FileExists(Exception):

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return "%s: File exists" % (self.filename,)


class MissArguments(Exception):

    def __str__(self):
        return "Miss arguments"


class WrongArgument(Exception):

    def __init__(self, index):
        self.index = index

    def __str__(self):
        return "WrongArgument at %d" % (self.index,)


class WrongOption(Exception):

    def __init__(self, option):
        self.index = option

    def __str__(self):
        return "WrongOption %s" % (self.option,)


class UserNotFound(Exception):

    def __init__(self, username):
        self.username = username

    def __str__(self):
        return 'User with name "%s" not found' % (self.username,)


class PermissionDenied(Exception):

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return "Permission denied: %s" % (self.filename,)


class IsADirectory(Exception):

    def __init__(self, filename):
        self.filename = filename

    def __str__(self):
        return "%s : is a directory" % (self.filename,)


class WrongArgumentsNum(Exception):

    def __init__(self, count):
        self.count = count

    def __str__(self):
        return "The number of arguments should be %d" % (self.count,)
