from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
import importlib
from .models import Folder
from .plugins.exceptions import FolderNotFound
import re
plugins = importlib.import_module(__package__+'.plugins')
# import copy
try:
    import simplejson as json
except:
    import json


class NoSuchCommand(Exception):

    def __str__(self):
        return "No such command"


def check_path(path, session, user):
    if Folder.objects.filter(path=path).exists() is True:
        # check superuser
        if user.is_superuser is True:
            return True

        folder = Folder.objects.get(path=path)
        # check host user
        if folder.user.username == user.username:
            return True
        # check host grp
        if folder.group in user.group.objects.all():
            if ((folder.mod >> 3) & 4) != 0:
                return True
            else:
                return False
        # check other
        if ((folder.mod >> 6) & 4) != 0:
            return True

        return False
    else:
        return False


def command_line_tool_ajax(request, path, command):
    if settings.DEBUG is True:
        try:
            user = User.objects.filter(is_superuser=True)[0]
        except Exception as e:
            raise e
            raise Exception("Please at least set one superuser")
    else:
        user = request.user

    args = re.split(r' +', command.strip())
    try:
        try:
            plugin = plugins.__dict__[args[0]]
        except Exception as e:
            raise NoSuchCommand()
        args.pop(0)
        path = '/' + path
        if check_path(path, request.session, user) is False:
            raise FolderNotFound(path)
        request.session['path'] = path
        msg = plugin.process(request.session, args)
    except Exception as e:
        raise e
        return HttpResponse(json.dumps({
            'status': 'error',
            'msg': str(e)}))
    return HttpResponse(json.dumps({'status': 'OK', "msg": msg}))


def command_line_tool(request):
    return render(request, 'command_line_tool.html', {})


if settings.DEBUG is False:
    command_line_tool_ajax = login_required(command_line_tool_ajax)
    command_line_tool = login_required(command_line_tool)
