from django.conf.urls import url

from . import views

app_name='bcs'
urlpatterns = [
    # ex: /
    url(r'^$', views.ListView.as_view(), name='list'),
    # ex: /ca/
    url(r'^(?P<pk>[^/]+)/$', views.DetailView.as_view(), name='detail'),
]
