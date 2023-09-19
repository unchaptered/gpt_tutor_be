from django.urls import include, path, re_path

# Controller
from api.v1.chats.controller.chat_controller import ChatController
from api.v1.chats.controller.chat_uuid_controller import ChatUuidController
from api.v1.chats.controller.cont_uuid_issolved_controller import ChatUuidIsSolvedController

urlpatterns = [
    path(
        route='',
        view=ChatController.as_view(),
        name='ChatController'
    ),
    path(
        route='/<str:chatUuid>',
        view=ChatUuidController.as_view(),
        name='ChatUuidController'
    ),
    path(
        route='/<str:chatUuid>/is-solved',
        view=ChatUuidIsSolvedController.as_view(),
        name='ChatUuidIsSolvedController'
    ),
]
