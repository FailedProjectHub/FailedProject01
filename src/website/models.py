from django.db import models
from cms.models import BaseFileAttrib, ListField
from video_cms.models import File

# Create your models here.


class VideoFileAttrib(BaseFileAttrib):
    uploader = models.ForeignKey('auth.User', db_index=True)
    video_file = models.ForeignKey(
        'video_cms.File',
        related_name="authattrib",
        db_index=True
    )
    hits = models.IntegerField(default=0)
    collected = models.IntegerField(default=0)


class SessionUploaderRecord(models.Model):
    session = models.OneToOneField(
        'video_cms.Session',
        related_name='session_uploader_record'
    )
    uploader = models.ForeignKey(
        'auth.User'
    )


class Danmaku(models.Model):
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(File, db_index=True, on_delete=models.PROTECT)
    mode = models.IntegerField()
    stime = models.IntegerField()
    date = models.PositiveIntegerField()
    text = models.CharField(max_length=128)
    size = models.IntegerField()
    color = models.CharField(max_length=16)

    @staticmethod
    def new(owner=None,
            date=None,
            mode=1,
            stime=0,
            text="",
            size=30,
            color=0xffffff):
        assert isinstance(owner, str) is True
        assert isinstance(mode, int) is True
        assert isinstance(stime, int) is True
        assert isinstance(text, str) is True
        assert isinstance(size, int) is True
        assert isinstance(color, str) is True
        assert isinstance(date, int) is True
        assert File.objects.filter(token=owner).count() == 1
        owner = File.objects.get(token=owner)
        Danmaku.objects.create(
            owner=owner,
            mode=mode,
            stime=stime,
            text=text,
            size=size,
            color=color,
            date=date
        )

    @staticmethod
    def load_danmaku_by_video_token(token):
        assert File.objects.filter(token=token).count() == 1
        video = File.objects.get(token=token)
        danmaku = list(
            map(lambda danmaku: {
                # 'owner': danmaku.owner,
                'mode': danmaku.mode,
                'stime': danmaku.stime,
                'text': danmaku.text,
                'size': danmaku.text,
                'color': danmaku.color,
                'date': danmaku.date
            }, video.danmaku_set.all())
        )
        return danmaku


class Comment(models.Model):
    id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(File, db_index=True, on_delete=models.PROTECT)
    created_at = models.DateTimeField()
    text = models.CharField(max_length=1024)


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


class AvatarPerInfo(BasePerInfo):
    avatar = models.ImageField(upload_to='avatar', null=True, blank=True)


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