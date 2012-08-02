'''
Created on 2.8.2012

@author: xaralis
'''
from django import template

from ella.core.models.publishable import Publishable

register = template.Library()


class MostCommonTagsNode(template.Node):
    def __init__(self, count, varname):
        self.count = count
        self.varname = varname

    def render(self, context):
        context[self.varname] = Publishable.tags.most_common()[:self.count]
        return ''


@register.tag
def get_most_common_tags(parser, token):
    try:
        tag_name, count, fill, varname = token.split_contents()
    except ValueError:
        try:
            tag_name, fill, varname = token.split_contents()
            count = 10
        except ValueError:
            raise template.TemplateSyntaxError('`get_most_common_tags` tag '
                                               'must follow form '
                                               '{% get_most_common_tags [COUNT] as [VARNAME] %}')

    return MostCommonTagsNode(count, varname)


class TagsForObjectNode(template.Node):
    def __init__(self, obj, varname):
        self.obj = template.Variable(obj)
        self.varname = varname

    def render(self, context):
        context[self.varname] = self.obj.resolve(context).tags.all()
        return ''


@register.tag
def tags_for_object(parser, token):
    try:
        tag_name, obj, fill, varname = token.split_contents()
        return TagsForObjectNode(obj, varname)
    except ValueError:
        raise template.TemplateSyntaxError('`tags_for_object` tag requires '
                                           'exactly 3 argument')
