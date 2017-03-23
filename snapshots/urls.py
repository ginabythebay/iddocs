from django.conf.urls import url

from . import views

app_name='snapshots'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^create/$', views.create, name='create'),
    url(r'^publish/$', views.publish, name='publish'),
]
