# from django.db.models.fields import Field
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import *

try:
    import simplejson as json
except:
    import json

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
            'avatar': (avatar_url is None) and "" or avatar_url
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
