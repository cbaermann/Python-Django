from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^shows$', views.shows),
    url(r'^shows/new$', views.new_show),
    url(r'^shows/(?P<showId>\d+)$', views.show_id),
    url(r'^shows/create', views.create_show),
    url(r'^shows/(?P<showId>\d+)/edit$', views.edit),
    url(r'^shows/(?P<showId>\d+)/edit_show$', views.edit_show),
    url(r'^shows/(?P<showId>\d+)/destroy$', views.destroy),

]