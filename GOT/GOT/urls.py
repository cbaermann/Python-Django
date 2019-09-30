from django.conf.urls import url, include


urlpatterns = [
    url(r'^', include('apps.got_app.urls')),
]
