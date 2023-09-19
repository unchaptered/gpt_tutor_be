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

        return self._getJsonResponse({
            'isSuccess': True
        })

    def post(self, request: HttpRequest):

        body = self._getRequestBody(request.body)
        gptAnswer = self.__talkService.sendQuestion(body['context'])

        return self._getJsonResponse({
            'isSuccess': True,
            'gptAnswer': gptAnswer
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
