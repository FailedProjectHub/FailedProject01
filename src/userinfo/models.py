from django.db import models
from cms.models import ListField

# Create your models here.


class BasePerInfoMetaclass(type(models.Model)):
    Register = {}

    def __init__(cls, name, base, nmspc):
        super(BasePerInfoMetaclass, cls).__init__(name, base, nmspc)
        BasePerInfoMetaclass.Register[name.lower()] = cls


class BasePerInfo(models.Model, metaclass=BasePerInfoMetaclass):
    user = models.OneToOneField('auth.User', related_name='%(class)s')

    class Meta:
        abstract = True

    def as_dict(self):
        ret = {}
        for k in self.display:
            ret[k] = self.__dict__[k]
        return ret


class GenericPerInfo(BasePerInfo):
    avatar = models.ImageField(upload_to='avatar')
    email = models.EmailField()

    display = ('avatar', 'email')


class AdvancedPerInfo(BasePerInfo):
    default_chunksize = models.IntegerField()
    default_path = ListField()

    display = ('default_chunksize', 'default_path')


class LoginLog(models.Model):
    user = models.ForeignKey('auth.User')
    login_ip = models.GenericIPAddressField()
    login_time = models.DateTimeField()


class VisitVideoLog(models.Model):
    user = models.ForeignKey('auth.User')
    visit_video = models.ForeignKey(
        'website.VideoFileAttrib', related_name='+')
    visit_time = models.DateTimeField()


class FocusRelation(models.Model):
    focus = models.ForeignKey(
        'auth.User', related_name='focus')
    focused = models.ForeignKey(
        'auth.User', related_name='focused')
