from django.shortcuts import get_object_or_404, render

from .models import BirthCertificate

def index(request):
    return HttpResponse("Hello, world. You're at the docs index.")

def bc_detail(request, location_id):
    return render(
        request,
        'docs/bc_detail.html',
        {'bc': get_object_or_404(BirthCertificate, pk=location_id)})
