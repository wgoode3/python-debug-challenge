## MESSAGEBOARD URLS
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^show(?P<id>[0-9]+)$', views.index, name = 'board' ),
    url(r'^message(?P<id>[0-9]+)$', views.createMessage, name = 'createMessage' ),
    url(r'^comment(?P<id>[0-9]+)$', views.createComment, name = 'createComment' ),
]
