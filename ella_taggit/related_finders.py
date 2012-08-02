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
        'content_object__publish_from__lte': datetime.now(),
        'content_object__published': True,
    }

    if mods:
        filters.update({
            'content_object__content_type__in': [ContentType.objects.get_for_model(m).pk for m in mods]
        })

    if only_from_same_site:
        filters.update({
            'content_object__category__site__pk': settings.SITE_ID
        })

    return collected_so_far + obj.tags.similar_objects(
        num=count - len(collected_so_far),
        filters=filters,
        excludes={'content_object__pk__in': [o.pk for o in collected_so_far]})
