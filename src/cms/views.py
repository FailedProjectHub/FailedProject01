from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.views.generic import View
from django.utils.decorators import method_decorator
import importlib
from .plugins.exceptions import *
from .plugins.base import *
import re
try:
    import simplejson as json
except:
    import json

plugins = importlib.import_module(__package__ + '.plugins').Register


class NoSuchCommand(Exception):

    def __str__(self):
        return "No such command"


def exec_command(environ, command):
    try:
        plugin = plugins[command[0]]
    except Exception:
        raise NoSuchCommand()
    command.pop(0)
    msg = plugin.process(environ, command)
    return HttpResponse(json.dumps({'status': 'OK', "msg": msg}))


def set_environ(user, path):
    environ = {}
    environ['user'] = user
    environ['username'] = user.username
    if not path.startswith('/'):
        raise Exception('Wrong path: path does not starts with "/"')
    if access(environ, path, AUTH_FOR_READ + AUTH_FOR_EXECUTE) is False:
        raise PermissionDenied(path)
    environ['path'] = path
    return environ


class command_line_tool_ajax(View):

    def post(self, request, *args, **kwargs):
        content = json.loads(request.body)
        try:
            assert 'command' in content
            assert isinstance(content['command'], list)
            assert 'path' in content
            assert isinstance(content['path'], str)
            environ = set_environ(request.user, content['path'])
            return exec_command(environ, content['command'])
        except Exception as e:
            return HttpResponse(json.dumps({
                'status': 'error',
                'msg': [[str(e)]]
            }))

    def get(self, request, path, command):
        path = '/' + path
        try:
            command = re.split(r' +', command.strip())
            environ = set_environ(request.user, path)
            return exec_command(environ, command)
        except Exception as e:
            raise e

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(command_line_tool_ajax, self).dispatch(
            request,
            *args,
            **kwargs
        )


@login_required
def command_line_tool(request):
    return render(request, 'command_line_tool.html', {})


if settings.DEBUG is False:
    command_line_tool_ajax = login_required(command_line_tool_ajax)
    command_line_tool = login_required(command_line_tool)
