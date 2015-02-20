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


class AbstractBasePerInfoMetaclass(type):

    Register = {}

    def __init__(cls, name, base, nmspc):
        super(AbstractBasePerInfoMetaclass, cls).__init__(name, base, nmspc)
        AbstractBasePerInfoMetaclass.Register[name] = cls


class AbstractBasePerInfo(object, metaclass=AbstractBasePerInfoMetaclass):
    pass


class MixinBasePerInfoModelMetaclass(type(models.Model), AbstractBasePerInfoMetaclass):
    pass


class BasePerInfo(models.Model, AbstractBasePerInfo,
                  metaclass=MixinBasePerInfoModelMetaclass):
    user = models.OneToOneField('auth.User', related_name='%(class)s')

    class Meta:
        abstract = True


class GenericPerInfo(BasePerInfo):
    avatar = models.ImageField(upload_to='avatar')
    email = models.EmailField()


class AdvancedPerInfo(BasePerInfo):
    default_chunksize = models.IntegerField()
    default_path = ListField()


class LoginLog(models.Model):
    user = models.ForeignKey('auth.User')
    login_ip = models.GenericIPAddressField()
    login_time = models.DateTimeField()


class VisitVideoLog(models.Model):
    user = models.ForeignKey('auth.User')
    visit_video = models.ForeignKey(
        'VideoFileAttrib', related_name='+')
    visit_time = models.DateTimeField()


class FocusRelation(models.Model):
    focus = models.ForeignKey(
        'auth.User', related_name='focus')
    focused = models.ForeignKey(
        'auth.User', related_name='focused')
