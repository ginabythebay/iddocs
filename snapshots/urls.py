from django.contrib import admin
from django.conf.urls import url

from . import views

app_name = 'snapshots'
urlpatterns = [
    url(r'^$', admin.site.admin_view(views.IndexView.as_view()), name='index'),
    url(r'^create/$', admin.site.admin_view(views.create), name='create'),
    url(r'^publish/$', admin.site.admin_view(views.publish), name='publish'),
]
