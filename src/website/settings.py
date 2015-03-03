from django.conf import settings
from os.path import dirname, isdir, exists
from os import makedirs
import os

DEFAULT_VIDEO_COVER_DIR = os.path.join(dirname(__file__), 'video_cover')
VIDEO_COVER_DIR = getattr(settings, 'VIDEO_COVER_DIR', DEFAULT_VIDEO_COVER_DIR)

if exists(VIDEO_COVER_DIR):
    if not isdir(VIDEO_COVER_DIR):
        raise ValueError('not a directory: %s' % VIDEO_COVER_DIR)
else:
    makedirs(VIDEO_COVER_DIR)
