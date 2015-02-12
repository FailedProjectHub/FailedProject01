from django.db import models
from cms.models import BaseFileAttrib

# Create your models here.


class VideoFileAttrib(BaseFileAttrib):
    uploader = models.OneToOneField('auth.User', db_index=True)
    video_file = models.OneToOneField('video_cms.File', db_index=True)

