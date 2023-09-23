from django.http import HttpRequest

from api.v1.base.base_controller import BaseController
from api.v1.chats.service.chat_service import ChatService


class ChatUuidController(BaseController):

    __chatService: ChatService

    def __init__(self):
        super().__init__()

        self.__chatService = ChatService()

    def get(self, request: HttpRequest, chatUuid: str):
        print('ChatUuidController : ' + request.path)
        hostUuid = 'sample'
        chat = self.__chatService.getChatByUuid(hostKey=hostUuid,
                                                chatUuid=chatUuid)

        return self._getJsonResponse({
            'isSuccess': True,
            'chat': chat
        })

    # def post(self, request: HttpRequest, chatUuid: str):
    #     print('ChatUuidController : ' + request.path)

    #     return self._getJsonResponse({
    #         'isSuccess': True
    #     })

    # def patch(self, request: HttpRequest, chatUuid: str):
    #     print('ChatUuidController : ' + request.path)

    #     return self._getJsonResponse({
    #         'isSuccess': True
    #     })

    # def put(self, request: HttpRequest, chatUuid: str):
    #     print('ChatUuidController : ' + request.path)

    #     return self._getJsonResponse({
    #         'isSuccess': True
    #     })

    def delete(self, request: HttpRequest, chatUuid: str):
        hostUuid = 'sample'
        chat = self.__chatService.delChatByUuid(hostKey=hostUuid,
                                                chatUuid=chatUuid)

        return self._getJsonResponse({
            'isSuccess': True
        })
