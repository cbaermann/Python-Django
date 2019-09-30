from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create_user$', views.create_user),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^new_job$', views.new_job),
    url(r'^cancel$', views.cancel),
    url(r'^(?P<userId>\d+)/create$', views.create_job),
    url(r'^jobs/(?P<jobId>\d+)$', views.view_job),
    url(r'^edit/(?P<jobId>\d+)$', views.edit_job),
    url(r'^(?P<jobId>\d+)/update$', views.update_job),
    url(r'^(?P<jobId>\d+)/remove$', views.remove_job),
    url(r'^logout$', views.logout),
]