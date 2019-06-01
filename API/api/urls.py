from django.conf.urls import url

from .views import Upload

urlpatterns = [
    url(r'^upload/', Upload.as_view(), name='upload'),
]
