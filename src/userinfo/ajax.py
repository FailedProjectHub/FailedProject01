import os
import io
from PIL import Image

from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from django.utils.decorators import method_decorator

from .models import *
from .settings import AVATAR_ROOT, AVATAR_SIZE_LIMIT

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
    assert 'ct' in request.GET
    op = int(request.GET['op'])
    ct = int(request.GET['ct'])
    if ct > 20:
        ct = 20
    return HttpResponse(json.dumps(list(map(
        lambda video: {
            'rec': video.video_file.rec,
            'filename': video.video_file.filename
        },
        VideoFileAttrib.objects.filter(uploader=request.user).order_by('video_file__rec')[op: ct + 1]
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
            with open(os.path.join(AVATAR_ROOT, request.user.username + '.png'), "rb") as f:
                return HttpResponse(f.read(), content_type='image/png')
        except Exception as e:
            raise e
            return HttpResponse(json.dumps({'status': 'error', 'reason': 'file not found'}))

    def patch(self, request):
        assert 'x1' in request.GET
        x1 = int(request.GET['x1'])
        assert 'y1' in request.GET
        y1 = int(request.GET['y1'])
        assert 'x2' in request.GET
        x2 = int(request.GET['x2'])
        assert 'y2' in request.GET
        y2 = int(request.GET['y2'])
        img = io.BytesIO(request.body)
        if img.seek(0, 2) > AVATAR_SIZE_LIMIT:
            return HttpResponse(
                {
                    "status": "error",
                    "reason": "Image size exceeds %d b" % (AVATAR_SIZE_LIMIT,)
                }
            )
        img.seek(0, 0)
        img = Image.open(img)
        img = img.crop((x1, y1, x2, y2))
        img.save(os.path.join(AVATAR_ROOT, request.user.username + '.png'))
        return HttpResponse({"status": "OK"})

    def post(self, request):
        with open(os.path.join(AVATAR_ROOT, request.user.username), "wb") as f:
            f.write(request.body)
        return HttpResponse(json.dumps({'status': 'OK'}))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(AvatarView, self).dispatch(*args, **kwargs)
