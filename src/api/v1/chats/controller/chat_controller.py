from typing import List
from django.http import HttpRequest

from api.v1.base.base_controller import BaseController
from api.v1.chats.service.chat_service import ChatService

from common.enums.gpt.e_gpt_instrucments import EGPT_INSTURMENTS

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
        
        body = self._getRequestBody(request.body)
        category = body['category']
        
        allowedCategory: List[str] = [ 'JAVA', 'JAVASCRIPT', 'KOTLIN', 'REACT', 'NEXT_JS', 'NODE_JS', 'NEST_JS', 'SPRING', 'CS', 'ETC' ]
        if not (category in allowedCategory):
            raise ValueError(f'category is not allowed except {allowedCategory}')
            
        chatUuid = self.__chatService.postChat(hostKey=hostUuid, category=category)

        return self._getJsonResponse({
            'isSuccess': True,
            'chat': {
                'chatUuid': chatUuid
            }
        })
