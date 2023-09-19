from django.urls import include, path, re_path

# Controller
from api.v1.talks.controller.talk_controller import TalkController

urlpatterns = [
    path(
        route='',
        view=TalkController.as_view(),
        name='TalkController'
    )
]
