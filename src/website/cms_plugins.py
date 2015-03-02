from cms.plugins.base import baseplugin
from cms.plugins import touch, lna
from .exceptions import *
from .models import *
from video_cms.models import *
from cms.plugins.exceptions import *
from cms.plugins.ls import ls
from optparse import OptionParser


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


class ils(baseplugin):

    parser = OptionParser()

    parser.add_option(
        "--sort", action="append",
        dest="sort")

    parser.add_option(
        "-r", dest="recursive",
        action="store_true",
        default="false")

    parser.add_option(
        "--op", dest="op",
        type="int")

    parser.add_option(
        "--ct", dest="ct",
        type="str")

    @staticmethod
    def process(environ, args):
        options, args = ils.parser.parse_args(args)
        new_args = []
        new_args.append('/'.join(['/public'] + args))
        if options.sort is not None:
            for sort in options.sort:
                if sort == "rec":
                    attrib = 'videofileattrib__video_file__rec'
                elif sort == "time":
                    attrib = "videofileattrib__video_file__created_at"
                elif sort == "cc":
                    attrib = "videofileattrib__click_counts"
                else:
                    raise WrongOption("--sort=%s" % (sort,))
                new_args.append('--sort=%s' % (attrib,))

        if options.op is None:
            options.op = 0
        new_args.append("--op=%d" % (options.op,))

        if options.ct is None:
            options.ct = 10
        new_args.append("--ct=%d" % (options.ct,))

        new_args.append("-l")
        new_args.append("-R")
        new_args.append("--ignore=folderattrib")
        new_args.append("--display=videofileattrib__video_file__rec")

        environ['user'].is_superuser = True
        res_list = ls.process(environ, new_args)
        environ['user'].is_superuser = False

        return res_list
