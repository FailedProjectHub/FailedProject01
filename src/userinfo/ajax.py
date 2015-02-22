# from django.db.models.fields import Field
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import *

try:
    import simplejson as json
except:
    import json

from cms.plugins.base import path_list_to_str
from website.models import *


@login_required
def genericperinfo(request):
    try:
        avatar_url = AvatarPerInfo.objects.get(user=request.user).avatar
    except AvatarPerInfo.DoesNotExist:
        return HttpResponse(json.dumps({
            'username': request.user.username,
            'email': request.user.email,
            'avatar': 'none'
        }))
    else:
        return HttpResponse(json.dumps({
            'username': request.user.username,
            'email': request.user.email,
            'avatar': avatar_url
        }))


@login_required
def advacedperinfo(request):
    info = AdvancedPerInfo.objects.get(user=request.user)
    return HttpResponse(json.dumps({
        'chunksize': info.default_chunksize,
        'path': path_list_to_str(info.default_path)
    }))


@login_required
def myupload(request):
    assert 'op' in request.GET
    assert 'ed' in request.GET
    return json.dumps(list(map(
        lambda video: [video.video_file.rec, 'none'],
        VideoFileAttrib.objects.filter(uploader=request.user).latest()[op:ed + 1]
    )))
