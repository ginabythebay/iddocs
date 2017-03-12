from django.views import generic

from .models import CourtOrder


class ListView(generic.ListView):
    template_name = 'cos/list.html'
    context_object_name = 'list'

    def get_queryset(self):
        """ Return the documents ordered by location name"""
        return CourtOrder.objects.order_by('location')


class DetailView(generic.DetailView):
    model = CourtOrder
    template_name = 'cos/detail.html'
    context_object_name = 'co'
