from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create_user$', views.create_user),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^shows', views.shows),
    url(r'^new_show$', views.new_show),
    url(r'^(?P<userId>\d+)/create$', views.create_show),
    url(r'^(?P<eventId>\d+)/view$', views.view),
    url(r'^(?P<eventId>\d+)/join$', views.join_event),
    url(r'^(?P<eventId>\d+)/delete$', views.delete_event),
    url(r'^logout$', views.logout),
]