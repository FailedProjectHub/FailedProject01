import os
import io
from PIL import Image
try:
    import simplejson as json
except Exception:
    import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import View
from video_cms.models import *
from django.contrib.auth.decorators import login_required

from cms.plugins.exceptions import *
import video_cms
from .models import *
from .cms_plugins import av
from .settings import (VIDEO_COVER_DIR,
    AVATAR_ROOT, AVATAR_SIZE_LIMIT)

av = av.process


class InitView(video_cms.upload_views.InitView):

    def post(self, request, data, *args, **kwargs):
        environ = {'user': request.user, 'username': request.user.username}
        try:
            response = super(InitView, self).post(
                request,
                data,
                *args,
                **kwargs
            )
            if response.status_code == 201:
                res_data = json.loads(response.content)
                session = Session.objects.get(token=res_data['token'])
                SessionUploaderRecord.objects.create(
                    session=session,
                    uploader=environ['user']
                )
            return response
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'error', 'msg': str(e)}))

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(InitView, self).dispatch(request, *args, **kwargs)


def auth_check(environ, owner):
    owner = Session.objects.get(token=owner)
    if owner.session_uploader_record.uploader.username \
            != environ['username']:
        raise Unauthorized("You are not the uploader")


class ChunkView(video_cms.upload_views.ChunkView):

    def put(self, request, owner, *args, **kwargs):
        environ = {'user': request.user, 'username': request.user.username}
        try:
            auth_check(environ, owner)
            response = super(ChunkView, self).put(
                request,
                owner,
                *args,
                **kwargs
            )
        except Exception as e:
            return HttpResponse(json.dumps({
                'errstr': str(e)
            }))
        return response

    def get(self, request, owner, *args, **kwargs):
        environ = {'user': request.user, 'username': request.user.username}
        try:
            auth_check(environ, owner)
            response = super(ChunkView, self).get(
                request,
                owner,
                *args,
                **kwargs
            )
        except Exception as e:
            return HttpResponse(json.dumps({
                'errstr': str(e)
            }))
        return response

    @method_decorator(login_required)
    def dispatch(self, request, owner, *args, **kwargs):
        return super(ChunkView, self).dispatch(request, owner, *args, **kwargs)


class FinalizeView(video_cms.upload_views.FinalizeView):
    def get(self, request, owner, *args, **kwargs):
        session = Session.objects.get(token=owner)
        filename = session.filename
        environ = {
            'user': request.user,
            'username': request.user.username,
        }
        try:
            auth_check(environ, owner)
            session.session_uploader_record.delete()
            response = super(FinalizeView, self).get(
                request,
                owner,
                *args,
                **kwargs
            )
            data = json.loads(response.content)
            data['path'] = '/home/' + str(request.user.username) + '/' + filename
            environ['path'] = data['path']
            if ('errstr' in data) is False:
                av(environ, [data['path'], str(data['rec'])])
            return response
        except Exception as e:
            raise e
            return HttpResponse(json.dumps({
                'errstr': str(e)
            }))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(FinalizeView, self).dispatch(*args, **kwargs)


class PageView(video_cms.upload_views.PageView):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PageView, self).dispatch(*args, **kwargs)


class DestroyView(video_cms.upload_views.DestroyView):

    def get(self, request, owner, *args, **kwargs):
        owner = owner.lower()
        environ = {'user': request.user, 'username': request.user.username}
        try:
            auth_check(environ, owner)
            return super(DestroyView, self).get(request, owner, *args, **kwargs)
        except Exception as e:
            raise e
            return HttpResponse(json.dumps({
                'errstr': str(e)
            }))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(DestroyView, self).dispatch(*args, **kwargs)


class SessionsView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        return HttpResponse(json.dumps(list(
            map(
                lambda record: {
                    'hash': record.session.filehash,
                    'filename': record.session.filename,
                    'size': record.session.size,
                    'token': record.session.token,
                    'chunksize': record.session.chunk_size
                },
                user.sessionuploaderrecord_set.order_by('id')
            )
        )))

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(SessionsView, self).dispatch(*args, **kwargs)


class DanmakuView(View):
    @staticmethod
    def get(request, token):
        danmaku_list = Danmaku.load_danmaku_by_video_token(token)
        return HttpResponse(json.dumps(danmaku_list))

    @staticmethod
    def post(request, token):
        try:
            data = request.POST
            assert isinstance(data, dict)
        except (ValueError, AssertionError):
            return HttpResponseBadRequest(
                {'errstr': 'invalid json format'},
                content_type='application/json'
            )

        assert 'mode' in data
        assert 'stime' in data
        assert 'text' in data
        assert 'color' in data
        assert 'size' in data
        assert 'date' in data
        Danmaku.new(
            owner=token,
            date=int(data['date']),
            mode=int(data['mode']),
            stime=int(data['stime']),
            text=data['text'],
            color=data['color'],
            size=int(data['size'])
        )
        return HttpResponse(json.dumps({'status': 'OK'}))


def load_index(request):
    args = json.loads(request.data)
    args = ['ils'] + args
    return run_command(request, args)


class VideoCoverView(View):

    def get(self, request, rec, *args, **kwargs):
        try:
            f = open(os.path.join(VIDEO_COVER_DIR, rec), "rb")
        except Exception:
            f = open(os.path.join(VIDEO_COVER_DIR, 'default'), "rb")
        return HttpResponse(f.read(), content_type='image')

    def post(self, request, rec, *args, **kwargs):
        try:
            video_ = VideoFileAttrib.objects.get(video_file__rec=int(rec))
        except Exception:
            return HttpResponse(json.dumps({
                'status': 'error',
                'reason': 'video file does not exists'
            }))
        if video_.uploader == request.user:
            with open(os.path.join(VIDEO_COVER_DIR, rec), "wb") as f:
                f.write(request.body)
            return HttpResponse(json.dumps({
                'status': 'OK'
            }))
        else:
            return HttpResponse(json.dumps({
                'status': 'error',
                'reason': 'Permission Denied: you are not the uploader'
            }))

    def dispatch(self, *args, **kwargs):
        return super(VideoCoverView, self).dispatch(*args, **kwargs)


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
            'filename': video.video_file.filename,
            'click_counts': video.hits
        },
        VideoFileAttrib.objects.filter(uploader=request.user).order_by('video_file__rec')[op: op + ct]
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