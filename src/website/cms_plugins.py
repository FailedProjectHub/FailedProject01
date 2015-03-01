from cms.plugins.base import baseplugin
from cms.plugins import touch, lna
from .exceptions import *
from .models import *
from video_cms.models import *
from cms.plugins.exceptions import *


class av(baseplugin):

    '''
        av path video_file_id
    '''

    @staticmethod
    def process(environ, args):
        options, args = av.parser.parse_args(args)
        try:
            path = args[0]
            video_file = args[1]
        except Exception:
            raise MissArguments()
        video_file = File.objects.get(rec=video_file)
        attrib = VideoFileAttrib.objects.create(
            uploader=environ['user'],
            video_file=video_file
        )
        touch.touch.process(environ, [path])
        return lna.lna.process(
            environ,
            ['website.videofileattrib', str(attrib.id), path]
        )
