from django.conf.urls import url

from . import views

app_name='feds'
urlpatterns = [
    # ex: /
    url(r'^$', views.ListView.as_view(), name='list'),
    # ex: /Passport/
    url(r'^(?P<pk>[^/]+)/$', views.DetailView.as_view(), name='detail'),
]
