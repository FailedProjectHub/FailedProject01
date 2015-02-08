from django.db import models
from django.utils.six import with_metaclass
import ast


class ListField(with_metaclass(models.SubfieldBase, models.TextField)):
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []
        if isinstance(value, list):
            return value
        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class File(models.Model):
    id = models.AutoField(primary_key=True)
    mod = models.IntegerField(default=0o700)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        'auth.User',
        related_name="%(class)s",
        blank=True,
        null=True,
        db_index=True)
    group = models.ForeignKey(
        'auth.Group',
        related_name="%(class)s",
        blank=True,
        null=True,
        db_index=True)
    parent_folder = models.ForeignKey(
        'File',
        related_name="sub_%(class)s",
        blank=True,
        null=True,
        db_index=True)
    path = ListField(blank=True, null=True, unique=True)

    def __str__(self):
        if len(self.path) == 1 and self.path[0] == '/':
            return '/'
        else:
            return r'/' + r'/'.join(self.path)


class BaseFileAttrib(models.Model):
    id = models.AutoField(primary_key=True)
    base_file = models.OneToOneField(File, related_name="%(class)s")

    def __str__(self):
        return self.base_file.__str__()

    class Meta:
        abstract = True


class FolderAttrib(BaseFileAttrib):
    pass


class LinkAttrib(BaseFileAttrib):
    size = models.BigIntegerField()
    filehash = models.CharField(max_length=64, unique=True)
    filename = models.CharField(max_length=1024)
    created_at = models.DateTimeField()
    finished_at = models.DateTimeField(auto_now_add=True)


class ACL(models.Model):
    r = models.BooleanField(default=False)
    w = models.BooleanField(default=False)
    file = models.ForeignKey('File', null=True, blank=True)
    user = models.ForeignKey('auth.User')
    group = models.ForeignKey('auth.Group')

    def save(self):
        if (self.file is None) + (self.folder is None) != 1:
            raise Exception("One and only one of file and folder can be set")
        if (self.group is None) + (self.user is None) != 1:
            raise Exception("One and only one of group and user can be set")
        super(ACL, self).__init__()
