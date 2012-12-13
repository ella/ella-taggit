'''
Created on 1.8.2012

@author: xaralis
'''
from django.template.defaultfilters import slugify
from django.views.generic import ListView
from django.conf import settings

from ella_taggit.models import PublishableTag, tag_list, publishables_with_tag
from ella.core.cache.utils import get_cached_object_or_404


class TaggedPublishablesView(ListView):
    context_object_name = 'listings'
    paginate_by = getattr(settings, 'TAG_LISTINGS_PAGINATE_BY', 10)
    relation_occ_threshold = getattr(settings, 'TAG_RELATION_OCCURENCE_THRESHOLD', None)
    relation_count_limit = getattr(settings, 'TAG_RELATION_COUNT_LIMIT', 5)

    def get_queryset(self, **kwargs):
        self.tag = get_cached_object_or_404(PublishableTag, slug=self.kwargs['tag'])
        return publishables_with_tag(self.tag, filters=kwargs)

    def get_template_names(self):
        return (
            'page/tagging/%s/listing.html' % slugify(self.kwargs['tag']),
            'page/tagging/listing.html',
        )

    def paginate_queryset(self, queryset, page_size):
        """
        Ella uses it's own pagination style. If you want django's style,
        delete this function.
        """
        paginator = self.get_paginator(queryset,
                                       page_size,
                                       allow_empty_first_page=self.get_allow_empty())

        if 'p' in self.request.GET and self.request.GET['p'].isdigit():
            page_no = int(self.request.GET['p'])
        else:
            page_no = 1

        page = paginator.page(page_no)
        return (paginator, page, page.object_list, page.has_other_pages())

    def get_context_data(self, **kwargs):
        context = super(TaggedPublishablesView, self).get_context_data(**kwargs)
        if context['is_paginated']:
            context['page'] = context['page_obj']
            context['results_per_page'] = self.paginate_by

        context['tag'] = self.tag
        context['related_tags'] = tag_list(self.object_list,
                                           threshold=self.relation_occ_threshold,
                                           count=self.relation_count_limit,
                                           omit=self.tag)
        return context
