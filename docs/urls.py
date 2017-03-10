from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /birth_certificates/ca/
    url(r'^birth_certificates/(?P<location_id>[^/]+)/$', views.bc_detail, name='bc_detail'),
]
