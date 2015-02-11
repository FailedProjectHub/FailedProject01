from django.conf.urls import patterns, include, url
from django.contrib import admin

import video_cms

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'ASA.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('cms.urls', namespace='cms')),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'admin/login.html'}),
    url(r'', include(video_cms)),
)
