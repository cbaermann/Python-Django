from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create_user),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^message/create', views.create_message),
    url(r'^message/(?P<messageId>\d+)/destroy$', views.delete_message),
    url(r'^comment/(?P<messageId>\d+)/create$', views.create_comment),
    url(r'^logout$', views.logout),

]