from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^create$', views.create_user),
    url(r'^login$', views.login),
    url(r'^books$', views.books),
    url(r'^add_book/(?P<userId>\d+)$', views.add_book),
    url(r'^book/(?P<bookId>\d+)$', views.view_book),
    url(r'^(?P<userId>\d+)/(?P<bookId>\d+)$', views.add_favorites),
    url(r'^(?P<userId>\d+)/(?P<bookId>\d+)/remove$', views.remove_favorites),
    url(r'^(?P<bookId>\d+)/update$', views.update_book),
    url(r'^(?P<bookId>\d+)/destroy$', views.delete),
    url(r'^logout$', views.logout),
]