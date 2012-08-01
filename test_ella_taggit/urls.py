from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'^tags/', include('ella_taggit.urls')),
    (r'^', include('ella.core.urls')),
)
