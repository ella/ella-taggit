# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.core.urlresolvers import reverse
from django.test import TestCase

from nose import tools

from ella.articles.models import Article
from ella.core.models.publishable import Publishable

from test_ella.test_core import create_basic_categories, create_and_place_a_publishable
from test_ella import template_loader

from ella_taggit.models import PublishableTag as Tag, PublishableTaggedItem as TaggedItem, \
    publishables_with_tag, tag_list


class TestTaggingViews(TestCase):
    def setUp(self):
        super(TestTaggingViews, self).setUp()
        create_basic_categories(self)
        create_and_place_a_publishable(self)

    def tearDown(self):
        super(TestTaggingViews, self).tearDown()
        template_loader.templates = {}

    def test_publishables_with_tag_returns_tagged_publishable(self):
        self.only_publishable.tags.set('tag1', 'tag2')
        tools.assert_equals(2, TaggedItem.objects.count())

        t = Tag.objects.get(name='tag1')
        tools.assert_equals([self.publishable], [p.target for p in publishables_with_tag(t)])

    def test_publishables_with_tag_doesnt_return_tagged_publishable_with_future_placement(self):
        self.only_publishable.tags.set('tag1', 'tag2')
        tools.assert_equals(2, TaggedItem.objects.count())

        self.publishable.publish_from = datetime.now() + timedelta(days=2)
        self.publishable.save()

        t = Tag.objects.get(name='tag1')
        tools.assert_equals([], list(publishables_with_tag(t)))

    def test_publishables_with_tag_returns_no_objects_when_none_tagged(self):
        t = Tag.objects.create(name='tag1')
        tools.assert_equals([], list(publishables_with_tag(t)))

    def test_tagged_publishables_view(self):
        self.only_publishable.tags.set('tag1', 'tag2')
        tools.assert_equals(2, TaggedItem.objects.count())

        t = Tag.objects.get(name='tag1')
        url = reverse('tag', kwargs={'tag': 'tag1'})
        template_loader.templates['page/tagging/listing.html'] = ''
        response = self.client.get(url)

        tools.assert_equals([self.publishable], [p.target for p in response.context['object_list']])
        tools.assert_equals(t, response.context['tag'])


class TestTagList(TestCase):
    def setUp(self):
        super(TestTagList, self).setUp()
        create_basic_categories(self)
        create_and_place_a_publishable(self)

    def test_tag_list_omits_if_requested(self):
        self.only_publishable.tags.set('tag1', 'tag2', 'tag3')
        t1 = Tag.objects.get(name='tag1')
        t2 = Tag.objects.get(name='tag2')
        t3 = Tag.objects.get(name='tag3')

        tools.assert_equals(list(tag_list([self.only_publishable])), [t3, t2, t1])
        tools.assert_equals(list(tag_list([self.only_publishable], omit=t1)), [t3, t2])

    def test_tag_list_limits_result_count(self):
        self.only_publishable.tags.set('tag1', 'tag2', 'tag3')
        tools.assert_equals(len(tag_list([self.only_publishable])), 3)
        tools.assert_equals(len(tag_list([self.only_publishable], count=2)), 2)

    def test_tag_list_adheres_to_threshold(self):
        self.pub = Article.objects.create(
            title=u'taglist2',
            slug=u'taglist2',
            description=u'taglist',
            category=self.category_nested,
            publish_from=datetime(2008, 1, 1),
            published=True
        )
        self.only_pub = self.pub.publishable_ptr

        self.only_publishable.tags.set('tag1', 'tag2', 'tag3')
        self.only_pub.tags.set('tag1', 'tag2')

        t1 = Tag.objects.get(name='tag1')
        t2 = Tag.objects.get(name='tag2')

        tools.assert_equals(tag_list([self.only_publishable, self.only_pub], threshold=2), [t2, t1])

    def test_tag_list_returns_items_in_order_of_occurence_count(self):
        self.pub = Article.objects.create(
            title=u'taglist2',
            slug=u'taglist2',
            description=u'taglist',
            category=self.category_nested,
            publish_from=datetime(2008, 1, 1),
            published=True
        )
        self.only_pub = self.pub.publishable_ptr

        self.pub2 = Article.objects.create(
            title=u'taglist3',
            slug=u'taglist3',
            description=u'taglist',
            category=self.category_nested,
            publish_from=datetime(2008, 5, 1),
            published=True
        )
        self.only_pub2 = self.pub2.publishable_ptr

        self.only_publishable.tags.set('tag1', 'tag2', 'tag3')
        self.only_pub.tags.set('tag1', 'tag2')
        self.only_pub2.tags.set('tag1')

        t1 = Tag.objects.get(name='tag1')
        t2 = Tag.objects.get(name='tag2')
        t3 = Tag.objects.get(name='tag3')

        tools.assert_equals(tag_list([self.only_publishable,
                                      self.only_pub,
                                      self.only_pub2]),
                                      [t1, t2, t3])
