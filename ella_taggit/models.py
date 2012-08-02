'''
Created on 1.8.2012

@author: xaralis
'''
from django.db import models
from django.utils.translation import ugettext_lazy as _

from ella.core.models import Publishable

from taggit.managers import TaggableManager
from taggit.models import ItemBase, TagBase


class PublishableTag(TagBase):
    description = models.TextField(verbose_name=_('Description'), blank=True,
                                   null=True)


class PublishableTaggedItem(ItemBase):
    tag = models.ForeignKey(PublishableTag, related_name="%(app_label)s_%(class)s_items")
    content_object = models.ForeignKey(Publishable)


# Patch Publishable class to have `tags` attribute
Publishable.tags = TaggableManager(through=PublishableTaggedItem)
