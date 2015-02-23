from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
import video_cms
from video_cms.models import *
from django.contrib.auth.decorators import login_required
from cms.plugins.exceptions import *
from .models import SessionUploaderRecord
from .cms_plugins import av
try:
    import simplejson as json
except Exception:
    import json

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

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(InitView, self).dispatch(request, *args, **kwargs)


def auth_check(environ, owner):
    owner = Session.objects.get(token=owner)
    if owner.session_uploader_record.uploader.username \
            != environ['username']:
        raise Unauthorized("You are not the uploader")


class ChunkView(video_cms.upload_views.ChunkView):

    @method_decorator(csrf_exempt)
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

    @method_decorator(csrf_exempt)
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
            if ('errstr' in data) is False:
                av(environ, [data['path'], str(data['rec'])])
            return response
        except Exception as e:
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
