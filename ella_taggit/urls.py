'''
Created on 1.8.2012

@author: xaralis
'''
from django.conf import settings
from django.conf.urls.defaults import patterns, url

from ella_taggit.views import TaggedPublishablesView


try:
    if getattr(settings, 'TAGGIT_CUSTOM_VIEWS', False):
        views = settings.TAGGIT_VIEWS
        temp = __import__(views, globals(), locals(), ['TaggedPublishablesView'])
        TaggedPublishablesView = temp.TaggedPublishablesView
except ImportError:
    pass

urlpatterns = patterns('',
    url(r'^(?P<tag>[-\w\s]+)/', TaggedPublishablesView.as_view(), name="tag"),
)
