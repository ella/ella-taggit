'''
Created on 1.2.2012

@author: xaralis
'''
from datetime import datetime

from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from ella.core.models import Publishable


def related_by_tags(obj, count, collected_so_far, mods=[], only_from_same_site=True):
    """
    Returns objects related to ``obj`` up to ``count`` by using tag
    relationship comparison (django-taggit's `similar_objects` method.
    """
    if isinstance(obj, Publishable):
        obj = obj.publishable_ptr

    filters = {
        'publish_from__lte': datetime.now(),
        'published': True,
        'pk__not__in': [o.pk for o in collected_so_far]
    }

    if mods:
        filters.update({
            'content_type__in': [ContentType.objects.get_for_model(m).pk for m in mods]
        })

    if only_from_same_site:
        filters.update({
            'category__site__pk': settings.SITE_ID
        })

    return collected_so_far + obj.tags.similar_objects(
        num=count + count - len(collected_so_far), **filters)
