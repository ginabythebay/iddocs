from django.core.urlresolvers import reverse

from bakery.views import BuildableDetailView, BuildableListView

from core.views import get_build_path

from .models import BirthCertificate


class ListView(BuildableListView):
    def __init__(self, **kwargs):
        super(ListView, self).__init__(**kwargs)
        ListView.build_path = get_build_path('bcs:list', 'index.html')

    template_name = 'bcs/list.html'
    context_object_name = 'list'

    def get_queryset(self):
        """ Return the documents ordered by location name"""
        return BirthCertificate.objects.order_by('location')


class DetailView(BuildableDetailView):
    model = BirthCertificate
    template_name = 'bcs/detail.html'
    context_object_name = 'bc'

    def get_url(self, obj):
        return reverse('bcs:detail', kwargs={'pk': obj.pk})
