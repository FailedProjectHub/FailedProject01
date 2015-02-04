from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# from django.core.exceptions import ValidationError


class File(models.Model):
    id = models.AutoField(primary_key=True)
    mod = models.IntegerField()
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
        'Folder',
        related_name="sub_%(class)s",
        blank=True,
        null=True,
        db_index=True)
    path = models.CharField(max_length=128, unique=True)
    attrib_type = models.ForeignKey(ContentType)
    attrib_id = models.PositiveIntegerField()
    attrib_object = GenericForeignKey('attrib_type', 'attrib_id')


class BaseFile(models.Model):
    id = models.AutoField(primary_key=True)

    class Meta:
        abstract = True


class Folder(BaseFile):

    def __str__(self):
        return str(self.path)


class VideoFile(BaseFile):
    size = models.BigIntegerField()
    filehash = models.CharField(max_length=64, unique=True)
    filename = models.CharField(max_length=1024)
    created_at = models.DateTimeField()
    finished_at = models.DateTimeField(auto_now_add=True)


class ACL(models.Model):
    r = models.BooleanField(default=False)
    w = models.BooleanField(default=False)
    folder = models.ForeignKey('Folder', null=True, blank=True)
    file = models.ForeignKey('File', null=True, blank=True)
    user = models.ForeignKey('auth.User')
    group = models.ForeignKey('auth.Group')

    def save(self):
        if (self.file is None) + (self.folder is None) != 1:
            raise Exception("One and only one of file and folder can be set")
        if (self.group is None) + (self.user is None) != 1:
            raise Exception("One and only one of group and user can be set")
        super(ACL, self).__init__()
