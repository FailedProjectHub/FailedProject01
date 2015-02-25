from django.conf.urls import patterns, url, include

from .ajax import *
from .views import *


urlpatterns_perinfo = patterns(
    r'',
    url(r'homepage/genericperinfo', genericperinfo),
    url(r'homepage/advancedperinfo', advacedperinfo),
    url(r'homepage/myupload/', myupload),
    url(r'homepage/mygroup/', mygroup),
    url(r'homepage/avatar/', AvatarView.as_view()),
)

urlpatterns_register = patterns(
    r'',
    url(r'register/', register.as_view())
)

urlpatterns_homepage = patterns(
    r'',
    url(r'homepage/', homepage)
)

urlpatterns = patterns(
    r'',
    url(r'', include(urlpatterns_perinfo)),
    url(r'', include(urlpatterns_register)),
    url(r'', include(urlpatterns_homepage)),
)
