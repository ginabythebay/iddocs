from django.shortcuts import render
from django.views import generic

from .models import BirthCertificate


class ListView(generic.ListView):
    template_name = 'bcs/list.html'
    context_object_name = 'list'

    def get_queryset(self):
        """ Return the documents ordered by location name"""
        return BirthCertificate.objects.order_by('location')


class DetailView(generic.DetailView):
    model = BirthCertificate
    template_name = 'bcs/detail.html'
    context_object_name = 'bc'
