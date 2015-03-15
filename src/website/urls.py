from django.conf.urls import patterns, url, include

from .views import *
from .ajax import *


urlpatterns_upload = patterns(
    r'',
    url(
        r'^upload/init/?',
        InitView.as_view(),
        name='init'
    ),

    url(
        r'^upload/chunk/(?P<owner>[a-fA-F0-9]{64})/?',
        ChunkView.as_view(),
        name='chunk'
    ),

    url(
        r'^upload/store/(?P<owner>[a-fA-F0-9]{64})/?',
        FinalizeView.as_view(),
        name='store'
    ),

    url(
        r'^upload/destroy/(?P<owner>[a-fA-F0-9]{64}/?)',
        DestroyView.as_view(),
        name='destroy'
    ),

    url(
        r'^upload/$',
        PageView.as_view(),
        name="upload"
    ),

    url(
        r'^upload/session/$',
        SessionsView.as_view(),
        name='sessions'
    )
)


urlpatterns_danmaku = patterns(
    '',
    url(
        r'danmaku/(?P<token>[a-zA-Z0-9]{64})/?',
        DanmakuView.as_view()
    ),
)


urlpatterns_index = patterns(
    '',
    url(
        r'^$',
        indexpage
    )
)

urlpatterns_video_cover = patterns(
    '',
    url(
        r'^video_cover/(?P<rec>[0-9]+)/$',
        VideoCoverView.as_view()
    )
)


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
    url(r'homepage/', homepage),
)


urlpatterns = patterns(
    r'',
    url(r'', include(urlpatterns_perinfo)),
    url(r'', include(urlpatterns_register)),
    url(r'', include(urlpatterns_homepage)),
    url(r'', include(urlpatterns_upload)),
    url(r'', include(urlpatterns_danmaku)),
    url(r'', include(urlpatterns_index)),
    url(r'', include(urlpatterns_video_cover)),
)
