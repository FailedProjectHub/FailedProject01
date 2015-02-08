from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
import importlib
from .plugins.exceptions import *
from .plugins.base import *
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


def command_line_tool_ajax(request, path, command):
    if settings.DEBUG is True:
        try:
            user = User.objects.filter(is_superuser=True)[0]
        except Exception as e:
            raise e
            raise Exception("Please at least set one superuser")
    else:
        user = request.user

    environ = {}
    environ['user'] = user
    environ['username'] = user.username
    # check access permission

    try:
        path = '/' + path
        if access(environ, path, AUTH_FOR_READ+AUTH_FOR_EXECUTE) is False:
            raise PermissionDenied(path)
        environ['path'] = path
        args = re.split(r' +', command.strip())
        try:
            plugin = plugins.__dict__[args[0]]
        except Exception as e:
            raise NoSuchCommand()
        args.pop(0)
        msg = plugin.process(environ, args)
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
