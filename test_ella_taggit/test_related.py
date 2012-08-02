from nose import tools

from ella.core.models import Related, Publishable

from ella_taggit.models import PublishableTag as Tag, PublishableTaggedItem as TaggedItem

from test_ella.test_core.test_related import GetRelatedTestCase


class TestGetRelatedWithtagging(GetRelatedTestCase):
    def setUp(self):
        super(TestGetRelatedWithtagging, self).setUp()
        self.Tag = Tag
        self.TaggedItem = TaggedItem

    def test_returns_object_with_similar_tags(self):
        self.only_publishable.tags.set('tag1', 'tag2')
        p = Publishable.objects.get(pk=self.publishables[0].pk)
        p.tags.set('tag1', 'tag2')
        tools.assert_equals([p], Related.objects.get_related_for_object(self.publishable, 1))


