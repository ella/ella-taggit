'''
Created on 1.8.2012

@author: xaralis
'''
import hashlib

import cPickle
from collections import defaultdict
from datetime import datetime
import operator

from django.db import models
from django.utils.translation import ugettext_lazy as _

from ella.core.models import Publishable
from ella.core.cache.utils import cache_this

from taggit.managers import TaggableManager, _TaggableManager
from taggit.models import ItemBase, TagBase
from taggit.utils import require_instance_manager


def get_tag_list_key(object_list, threshold, count, omit):
    return 'ella_taggit.models.tag_list:%s:%d:%d:%d' % (
        hashlib.md5(','.join([str(o.pk) for o in object_list])).hexdigest(),
        threshold or 0,
        count or 0,
        omit.pk)


@cache_this(get_tag_list_key)
def tag_list(object_list, threshold=None, count=None, omit=None):
    """
    Returns all tags appearing for any object in `object_list` ordered
    by their occurence.

    Optionally, max `count` can be specified and also a `threshold` which have
    to be met if a tag would be in the result list.

    Moreover, if you specify `omit` argument by supplying `PublishableTag`
    instance, this tag (if present in results) will be omitted.
    """
    occ_map = defaultdict(int)
    tags = PublishableTag.objects.filter(
        tagged_items__content_object__in=object_list)

    if omit is not None:
        tags = tags.exclude(pk=omit.pk)

    for t in tags:
        occ_map[t] += 1

    if threshold is not None:
        occ_map = dict((tag, occ)
                       for tag, occ in occ_map.iteritems()
                       if occ >= threshold)

    tag_list = map(operator.itemgetter(0),
                   reversed(sorted(occ_map.items(), key=lambda i: i[1])))

    if count is not None:
        tag_list = tag_list[:count]

    return tag_list


@cache_this(lambda tag, **kwargs: u'ella_taggit.models.pub_w_t:%s:%s' % (
    u';'.join([t.slug for t in sorted(tag, key=lambda i: i.id)]) if hasattr(tag, '__iter__') else tag.slug,
    hashlib.md5(cPickle.dumps(sorted(kwargs.iteritems()))).hexdigest()
))
def publishables_with_tag(tag=(), filters={}, excludes={}):
    now = datetime.now()

    if not hasattr(tag, '__iter__'):
        tag = [tag]

    qset = Publishable.objects.filter(
        models.Q(publish_to__isnull=True) | models.Q(publish_to__gt=now),
        publish_from__lt=now,
        published=True,
        tags__in=tag,
        **filters
    )

    if excludes:
        qset = qset.exclude(**excludes)

    return qset.distinct().order_by('-publish_from')


class PublishableTag(TagBase):
    description = models.TextField(verbose_name=_('Description'), blank=True,
                                   null=True)

    class Meta:
        verbose_name = _('Publishable tag')
        verbose_name_plural = _('Publishable tags')

    @models.permalink
    def get_absolute_url(self):
        return ('tag', [self.slug])


class PublishableTaggedItem(ItemBase):
    tag = models.ForeignKey(PublishableTag, related_name="tagged_items")
    content_object = models.ForeignKey('core.Publishable')

    class Meta:
        verbose_name = _('Tagged item')
        verbose_name_plural = _('Tagged items')

    @classmethod
    def tags_for(cls, model, instance=None):
        if instance is not None:
            return cls.tag_model().objects.filter(**{
                '%s__content_object' % cls.tag_relname(): instance
            })
        return cls.tag_model().objects.filter(**{
            '%s__content_object__isnull' % cls.tag_relname(): False
        }).distinct()


# Since django-taggit doesn't support excludes attibute in `similar_objects`
# method so far, provide an alternative which is also a little faster.
class _PublishableTaggableManager(_TaggableManager):
    @require_instance_manager
    def similar_objects(self, num=None, filters={}, excludes={}):
        lookup_kwargs = self._lookup_kwargs()

        qs = self.through.objects.all()

        if excludes is not None:
            lookup_kwargs.update(**excludes)

        qs = qs.annotate(n=models.Count('pk'))
        qs = qs.exclude(**lookup_kwargs)

        subq = self.all()

        qs = qs.filter(tag__in=list(subq))
        qs = qs.order_by('-n')

        if filters is not None:
            qs = qs.filter(**filters)

        if num is not None:
            qs = qs[:num]

        return list(set(pti.content_object for pti in qs))


class PublishableTaggableManager(TaggableManager):
    def __get__(self, instance, model):
        if instance is not None and instance.pk is None:
            raise ValueError("%s objects need to have a primary key value "
                "before you can access their tags." % model.__name__)
        manager = _PublishableTaggableManager(
            through=self.through, model=model, instance=instance
        )
        return manager


from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["ella_taggit.models.PublishableTaggableManager"])

# Patch Publishable class to add `tags` attribute
Publishable.add_to_class('tags', PublishableTaggableManager(through=PublishableTaggedItem))
