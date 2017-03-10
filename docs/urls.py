from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /birth_certificates/ca/
    url(r'^birth_certificates/(?P<pk>[^/]+)/$', views.BCDetailView.as_view(), name='bc_detail'),

    # ex: /court_orders/ca/
    url(r'^court_orders/(?P<pk>[^/]+)/$', views.CODetailView.as_view(), name='co_detail'),
]
