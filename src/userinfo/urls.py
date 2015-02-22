from django.conf.urls import patterns, url, include

from .ajax import *
from .views import *


urlpatterns_perinfo = patterns(
    r'',
    url(r'homepage/genericperinfo', genericperinfo),
    url(r'homepage/advacedperinfo', advacedperinfo),
    url(r'hompage/myupload/', myupload),
)

urlpatterns_register = patterns(
    r'',
    url(r'register/', register.as_view())
)

urlpatterns = patterns(
    r'',
    url(r'', include(urlpatterns_perinfo)),
    url(r'', include(urlpatterns_register))
)
