from django.urls import include, path, re_path

# Controller
from api.v1.base.base_controller import BaseController

urlpatterns = [
    path('', BaseController.as_view(), name='BaseController'),
    path('api/v1/chats', include('api.v1.chats.chats_router')),
    path('api/v1/talks', include('api.v1.talks.talks_router'))
]
