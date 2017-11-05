from django.conf.urls import url, include
import django.contrib.auth.urls
# from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url(r'^$', views.index, name='index'),
    # url(r'^login/$', auth_views.login, name='login'),
    # url(r'^logout/$', auth_views.logout, name='logout'),
]