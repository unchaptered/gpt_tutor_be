from django.http import HttpRequest

from api.v1.base.base_controller import BaseController
from api.v1.chats.service.chat_service import ChatService


class ChatController(BaseController):

    def __init__(self):
        super().__init__()

        self.__chatService = ChatService()

    def get(self, request: HttpRequest):
        hostUuid = 'sample'
        chats = self.__chatService.getAllChats(hostKey=hostUuid)

        return self._getJsonResponse({
            'isSuccess': True,
            'chatList': chats
        })

    def post(self, request: HttpRequest):
        hostUuid = 'sample'
        chatUuid = self.__chatService.postChat(hostKey=hostUuid)

        return self._getJsonResponse({
            'isSuccess': True,
            'chat': {
                'chatUuid': chatUuid
            }
        })
