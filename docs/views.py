from django.shortcuts import get_object_or_404, render

from .models import BirthCertificate, CourtOrder

def index(request):
    return HttpResponse("Hello, world. You're at the docs index.")

def bc_detail(request, location_id):
    return render(
        request,
        'docs/bc_detail.html',
        {'bc': get_object_or_404(BirthCertificate, pk=location_id)})

def co_detail(request, location_id):
    return render(
        request,
        'docs/co_detail.html',
        {'co': get_object_or_404(CourtOrder, pk=location_id)})
