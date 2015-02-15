from django.db import models
from cms.models import BaseFileAttrib

# Create your models here.


class VideoFileAttrib(BaseFileAttrib):
    uploader = models.ForeignKey('auth.User', db_index=True)
    video_file = models.OneToOneField(
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
