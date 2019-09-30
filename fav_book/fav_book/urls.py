from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('apps.fav_book_app.urls')),
]
