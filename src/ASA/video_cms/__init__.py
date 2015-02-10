from django.conf.urls import patterns, url, include
from .upload_views import InitView, ChunkView, FinalizeView, DestroyView, PageView
from .player_views import MediaView, DownloadView, DanmakuView
from django.views.decorators.csrf import csrf_exempt

__all__ = ['exceptions', 'models', 'views']

urlpatterns_upload = patterns('upload/',
        url('init/?', csrf_exempt(InitView.as_view()), name='init'),
        url('chunk/(?P<owner>[a-fA-F0-9]{64})/?', csrf_exempt(ChunkView.as_view()), name='chunk'),
        url('store/(?P<owner>[a-fA-F0-9]{64})/?', csrf_exempt(FinalizeView.as_view()), name='store'),
        url('destroy/(?P<owner>[a-fA-F0-9]{64}/?)', csrf_exempt(DestroyView.as_view()), name='destroy'),
        url('', PageView.as_view(), name="upload")
)

urlpatterns_download = patterns('',
        url(r'rec/(?P<filename>[a-zA-Z0-9_]{1,64})/?', MediaView.as_view()),
        url(r'download/(?P<token>[a-zA-Z0-9]{64})/?', DownloadView.as_view())
)

urlpatterns_danmaku = patterns('',
        url(r'danmaku/(?P<token>[a-zA-Z0-9]{64})/?', csrf_exempt(DanmakuView.as_view())),
)


urlpatterns = patterns('',
        url('', include(urlpatterns_upload)),
        url('', include(urlpatterns_download)),
        url('', include(urlpatterns_danmaku)),
)
