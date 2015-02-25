import os

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator

from .models import *
from .settings import AVATAR_ROOT

try:
    import simplejson as json
except:
    import json

from website.models import *


@login_required
def genericperinfo(request):
    return HttpResponse(json.dumps({
        'username': request.user.username,
        'email': request.user.email,
    }))


@login_required
def advacedperinfo(request):
    info = AdvancedPerInfo.objects.get(user=request.user)
    return HttpResponse(json.dumps({
        'chunksize': info.default_chunksize,
    }))


@login_required
def myupload(request):
    assert 'op' in request.GET
    assert 'ed' in request.GET
    op = int(request.GET['op'])
    ed = int(request.GET['ed'])
    return HttpResponse(json.dumps(list(map(
        lambda video: [video.video_file.rec, 'none'],
        VideoFileAttrib.objects.filter(uploader=request.user).order_by('video_file__created_at')[op:ed + 1]
    ))))


@login_required
def mygroup(request):
    return HttpResponse(json.dumps(
        list(map(
            lambda group: group.name,
            request.user.groups.all()
        ))
    ))


class AvatarView(View):

    def get(self, request):
        try:
            with open(os.path.join(AVATAR_ROOT, request.user.username), "rb") as f:
                return HttpResponse(f.read(), content_type='image/jpeg')
        except Exception as e:
            raise e
            return HttpResponse(json.dumps({'status': 'error', 'reason': 'file not found'}))

    def post(self, request):
        with open(os.path.join(AVATAR_ROOT, request.user.username), "wb") as f:
            f.write(request.body)
        return HttpResponse(json.dumps({'status': 'OK'}))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AvatarView, self).dispatch(*args, **kwargs)
