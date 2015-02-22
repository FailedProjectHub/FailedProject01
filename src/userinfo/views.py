from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User

from video_cms.settings import MIN_CHUNK_SIZE

try:
    import simplejson as json
except Exception:
    import json
from .models import *

# Create your views here.


class register(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'register.html')

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        assert 'username' in data
        assert 'password' in data
        assert 'email' in data
        try:
            User.objects.get(username=data['username'])
        except User.DoesNotExist:
            pass
        else:
            return HttpResponse(json.dumps({"status": "error", "msg": "duplicated"}))
        user = User.objects.create(
            username=data['username'],
            password=data['password'],
            email=data['email']
        )
        AvatarPerInfo.objects.create(
            user=user
        )
        AdavancedPerInfo.objects.create(
            user=user,
            default_chunksize=MIN_CHUNK_SIZE,
            default_path=['home', user.username]
        )
        return HttpResponse(json.dumps({"status": "OK"}))

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_active:
            return HttpResponse("please first logout")
        else:
            return super(register, self).dispatch(request, *args, **kwargs)
