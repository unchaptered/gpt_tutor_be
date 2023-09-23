from django.http import HttpRequest

# layers
from api.v1.base.base_controller import BaseController
from api.v1.talks.service.talk_service import TalkService


class TalkController(BaseController):

    __talkService: TalkService

    def __init__(self):
        super().__init__()
        self.__talkService = TalkService()

    def get(self, request: HttpRequest):
        print('TalkController : ' + request.path)
        
        body = self._getRequestBody(request.body)
        chatUuid = request.GET['chatUuid']
        talkUuid = request.GET['talkUuid']
        self.__talkService.getTalk(chatUuid=chatUuid,
                                   talkUuid=talkUuid)

        return self._getJsonResponse({
            'isSuccess': True
        })

    def post(self, request: HttpRequest):
        print('TalkController : ' + request.path)

        body = self._getRequestBody(request.body)
        chatUuid = body['chatUuid']
        context = body['context']
        talkUuid = self.__talkService.postTalk(chatUuid=chatUuid,
                                                context=context)
        # gptAnswer = self.__talkService.sendQuestion(chatUuid=chatUuid,
        #                                             context=context)

        return self._getJsonResponse({
            'isSuccess': True,
            'talk': {
                'talkUuid': talkUuid
            }
        })

    def patch(self, request: HttpRequest):
        print('TalkController : ' + request.path)

        return self._getJsonResponse({
            'isSuccess': True
        })

    def put(self, request: HttpRequest):
        print('TalkController : ' + request.path)

        return self._getJsonResponse({
            'isSuccess': True
        })

    def delete(self, request: HttpRequest):
        print('TalkController : ' + request.path)

        return self._getJsonResponse({
            'isSuccess': True
        })
