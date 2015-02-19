from django.db import models
from cms.models import BaseFileAttrib, ListField

# Create your models here.


class VideoFileAttrib(BaseFileAttrib):
    uploader = models.ForeignKey('auth.User', db_index=True)
    video_file = models.ForeignKey(
        'video_cms.File',
        related_name="authattrib",
        db_index=True
    )


class SessionUploaderRecord(models.Model):
    session = models.OneToOneField(
        'video_cms.Session',
        related_name='session_uploader_record'
    )
    uploader = models.ForeignKey(
        'auth.User'
    )


class BasePerInfoMetaclass(type):

    Register = {}

    def __init__(cls, name, base, nmspc):
        super(BasePerInfoMetaclass, cls).__init__(name, name, base, nmspc)
        BasePerInfoMetaclass.Register[name] = cls


class BasePerInfo(models.Model, metaclass=BasePerInfoMetaclass):

    user = models.OneToOneField('auth.User', related_name='%(class)s')

    class Meta:
        Abstract = True


class GenericPerInfo(BasePerInfo):
    avatar = models.ImageField(upload_to='avatar')
    email = models.EmailField()


class AdvancedPerInfo(BasePerInfo):
    default_chunksize = models.IntegerField()
    default_path = ListField()


class SystemLogPerInfo(BasePerInfo):
    pass


class LoginLog(models.Model):
    systemlogperinfo = models.foreignkey('SystemLogPerInfo')
    login_ip = models.GenericIPAddressField()
    login_time = models.DateTimeField()


class VisitVideoLog(models.Model):
    systemlogperinfo = models.Foreignkey('SystemLogPerInfo')
    visit_video = models.ForeignKey(
        'VideoFileAttrib', related_name='+')
    visit_time = models.DateTimeField()


class FocusRelation(models.Model):
    focus = models.ForeignKey(
        'auth.User', related_name='+')
    focused = models.ForeignKey(
        'auth.User', related_name='+')
