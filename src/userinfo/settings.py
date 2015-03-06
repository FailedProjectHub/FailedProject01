from django.conf import settings
from os.path import dirname, isdir, exists
from os import makedirs
import os

AVATAR_SIZE_LIMIT = 524288

DEFAULT_AVATAR_ROOT = os.path.join(dirname(__file__), 'avatar/')
AVATAR_ROOT = getattr(settings, 'AVATAR_ROOT', DEFAULT_AVATAR_ROOT)

if exists(AVATAR_ROOT):
    if not isdir(AVATAR_ROOT):
        raise ValueError('not a directory: %s' % AVATAR_ROOT)
else:
    makedirs(AVATAR_ROOT)

DEFAULT_INDEX = '/'
INDEX = getattr(settings, 'INDEX', DEFAULT_INDEX)
settings.INDEX = INDEX
