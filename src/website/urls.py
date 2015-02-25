from django.conf.urls import patterns, url, include
from .views import *


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


urlpatterns = patterns(
    r'',
    url(r'', include(urlpatterns_upload)),
<<<<<<< HEAD
=======
    url(r'', include(urlpatterns_danmaku))
>>>>>>> master
)
