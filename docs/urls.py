from django.conf.urls import url

from . import views

app_name='docs'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /birth_certificates/ca/
    url(r'^birth_certificates/(?P<pk>[^/]+)/$', views.BCDetailView.as_view(), name='bc_detail'),

    # ex: /court_orders/ca/
    url(r'^court_orders/(?P<pk>[^/]+)/$', views.CODetailView.as_view(), name='co_detail'),

    # ex: /fed_docs/
    url(r'^fed_docs/$', views.FedListView.as_view(), name='fed_list'),
    # ex: /fed_docs/Passport/
    url(r'^fed_docs/(?P<pk>[^/]+)/$', views.FedDetailView.as_view(), name='fed_detail'),
]
