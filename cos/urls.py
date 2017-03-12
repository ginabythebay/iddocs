from django.conf.urls import url

from . import views

app_name='cos'
urlpatterns = [
    # ex: /
    url(r'^$', views.ListView.as_view(), name='list'),
    # ex: /ca/
    url(r'^court_orders/(?P<pk>[^/]+)/$', views.DetailView.as_view(), name='detail'),
]
