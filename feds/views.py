from django.core.urlresolvers import reverse

from bakery.views import BuildableDetailView, BuildableListView

from core.views import get_build_path

from .models import FederalDoc


class ListView(BuildableListView):
    def __init__(self, **kwargs):
        super(ListView, self).__init__(**kwargs)
        ListView.build_path = get_build_path('feds:list', 'index.html')

    template_name = 'feds/list.html'
    context_object_name = 'list'

    def get_queryset(self):
        """ Return the documents ordered by name"""
        return FederalDoc.objects.order_by('name')


class DetailView(BuildableDetailView):
    model = FederalDoc
    template_name = 'feds/detail.html'
    context_object_name = 'fed'

    def get_url(self, obj):
        return reverse('feds:detail', kwargs={'pk': obj.pk})
