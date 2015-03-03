from django.conf.urls import url, patterns
from .views import command_line_tool, command_line_tool_ajax


urlpatterns = patterns(
    '',
    url(
        r"^cms/(?P<path>(([a-z0-9A-Z-_]+/)*))(?P<command>([a-z0-9A-Z-_ /.=-])*)$",
        command_line_tool_ajax.as_view(),
        name="command_line_tool"
    ),
    url(r"^cms_command_line_tool/", command_line_tool)
)
