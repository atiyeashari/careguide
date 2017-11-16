from django.conf.urls import url, include
import django.contrib.auth.urls
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='login.html', redirect_field_name='index'), name='login'),
    # url(r'^$', views.index, name='index'),
    url(r'^accounts/profile/$', views.index, name='index'),
    url(r'^deleteBooking/$', views.delete_booking, name='delete_booking'),
    url(r'^deleteAvailability/$', views.delete_availability, name='delete_availability'),
    url(r'^deleteAvailability/$', views.baby_sitter_add_availability, name='baby_sitter_add_availability')
]