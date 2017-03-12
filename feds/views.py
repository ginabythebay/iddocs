from django.views import generic

from .models import FederalDoc


class ListView(generic.ListView):
    template_name = 'feds/list.html'
    context_object_name = 'list'

    def get_queryset(self):
        """ Return the documents ordered by name"""
        return FederalDoc.objects.order_by('name')


class DetailView(generic.DetailView):
    model = FederalDoc
    template_name = 'feds/detail.html'
    context_object_name = 'fed'
