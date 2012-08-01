'''
Created on 1.8.2012

@author: xaralis
'''
from django.conf.urls.defaults import patterns, url

from ella_taggit.views import TaggedPublishablesView


urlpatterns = patterns('',
    url(r'^(?P<tag>[-\w\s]+)/', TaggedPublishablesView.as_view(), name="tag_list"),
)
