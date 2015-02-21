from django.conf.urls import patterns, url, include

from .ajax import *
from .views import *


urlpatterns_perinfo = patterns(
    r'',
    url(r'^profile/ajax/(?P<infotype>[a-zA-Z0-9]+)$/?', PerInfoAJAX)
)

urlpatterns_register = patterns(
    r'',
    url(r'^register$', register.as_view())
)

urlpatterns = patterns(
    r'',
    url(r'', include(urlpatterns_perinfo)),
    url(r'', include(urlpatterns_register))
)
