from django.shortcuts import render
from django.http import HttpResponseBadRequest, \
    HttpResponse
from video_cms import views
from django.contrib.auth.decorators import login_required
from cms.models import *
from cms.plugins.exceptions import *
from cms.plugins.base import access, path_str_to_list
try:
    import simplejson as json
except Exception:
    import json

# Create your views here.


@login_required
class InitView(views.InitView):

    def post(self, request, data, *args, **kwagrs):
        try:
            assert 'path' in data
        except Exception:
            return HttpResponseBadRequest(
                json.dumps(
                    {'errstr': 'required field missing'}
                ),
                content_type='application/json'
            )
        environ = {'user': request.user, 'username': request.user.username}
        path_list = path_str_to_list(data['path'])
        folder_path_list = path_list[:-1]
        try:
            if access(environ, folder_path_list, 0o2) is False:
                raise Unauthorized("Permission Denied")
            av(environ, ["init", data['path']])
            return super(InitView, self).post(request, *args, **kwargs)
        except Exception as e:
            return HttpResponse(json.dumps({'status': 'error', 'msg': str(e)}))

    @login_required
    def dispatch(self, request, *args, **kwargs):
        super(InitView, self).dispatch(request, *args, **kwargs)
