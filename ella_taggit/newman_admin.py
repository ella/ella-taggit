import ella_newman as newman
from ella_newman.conf import newman_settings

from django.utils.translation import ugettext_lazy as _

from ella_taggit.models import PublishableTag, PublishableTaggedItem


class TaggingInlineAdmin(newman.NewmanTabularInline):
    model = PublishableTaggedItem
    max_num = newman_settings.MAX_TAGS_INLINE
    suggest_fields = {'tag': ('name',)}
#    formset = TaggingInlineFormset


class TagAdmin(newman.NewmanModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'slug')


class TaggedItemAdmin(newman.NewmanModelAdmin):
    list_display = ('content_object', 'tag',)
    search_fields = ('tag',)
    suggest_fields = {'tag': ('name',)}

newman.site.register(PublishableTag, TagAdmin)
newman.site.register(PublishableTaggedItem, TaggedItemAdmin)
newman.site.append_inline(newman.site.MODELS_ALL_PUBLISHABLE, TaggingInlineAdmin)

# some translations for newman:

app = _('Tagging')
sg, pl = _('tag'), _('tags')
