from django.views import generic

from .models import BirthCertificate, CourtOrder

def index(request):
    return HttpResponse("Hello, world. You're at the docs index.")


class BCDetailView(generic.DetailView):
    model = BirthCertificate
    template_name = 'docs/bc_detail.html'


class CODetailView(generic.DetailView):
    model = CourtOrder
    template_name = 'docs/co_detail.html'
