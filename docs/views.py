from django.views import generic

from .models import BirthCertificate, CourtOrder, FederalDoc

def index(request):
    return HttpResponse("Hello, world. You're at the docs index.")


class BCDetailView(generic.DetailView):
    model = BirthCertificate
    template_name = 'docs/bc_detail.html'
    context_object_name = 'bc'


class COListView(generic.ListView):
    template_name = 'docs/co_list.html'
    context_object_name = 'list'

    def get_queryset(self):
        """ Return the documents ordered by name"""
        return CourtOrder.objects.order_by('location')


class CODetailView(generic.DetailView):
    model = CourtOrder
    template_name = 'docs/co_detail.html'
    context_object_name = 'co'


class FedListView(generic.ListView):
    template_name = 'docs/fed_list.html'
    context_object_name = 'docs'

    def get_queryset(self):
        """ Return the documents ordered by name"""
        return FederalDoc.objects.order_by('name')


class FedDetailView(generic.DetailView):
    model = FederalDoc
    template_name = 'docs/fed_detail.html'
    context_object_name = 'fed'
