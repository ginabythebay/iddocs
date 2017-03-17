from django.core.urlresolvers import reverse

from bakery.views import BuildableDetailView, BuildableListView

from core.views import get_build_path

from .models import CourtOrder


class ListView(BuildableListView):
    def __init__(self, **kwargs):
        super(ListView, self).__init__(**kwargs)
        ListView.build_path = get_build_path('cos:list', 'index.html')

    template_name = 'cos/list.html'
    context_object_name = 'list'

    def get_queryset(self):
        """ Return the documents ordered by location name"""
        return CourtOrder.objects.order_by('location')


class DetailView(BuildableDetailView):
    model = CourtOrder
    template_name = 'cos/detail.html'
    context_object_name = 'co'

    def get_url(self, obj):
        return reverse('cos:detail', kwargs={'pk': obj.pk})
