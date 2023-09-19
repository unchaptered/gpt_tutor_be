from django.http import HttpRequest

from api.v1.base.base_controller import BaseController


class ChatUuidIsSolvedController(BaseController):

    def get(self, request: HttpRequest, chatUuid: str):
        print('ChatUuidIsSolvedController : ' + request.path)

        return self._getJsonResponse({
            'isSuccess': True
        })

    def post(self, request: HttpRequest, chatUuid: str):
        print('ChatUuidIsSolvedController : ' + request.path)

        return self._getJsonResponse({
            'isSuccess': True
        })

    def patch(self, request: HttpRequest, chatUuid: str):
        print('ChatUuidIsSolvedController : ' + request.path)

        return self._getJsonResponse({
            'isSuccess': True
        })

    def put(self, request: HttpRequest, chatUuid: str):
        print('ChatUuidIsSolvedController : ' + request.path)

        return self._getJsonResponse({
            'isSuccess': True
        })

    def delete(self, request: HttpRequest, chatUuid: str):
        print('ChatUuidIsSolvedController : ' + request.path)

        return self._getJsonResponse({
            'isSuccess': True
        })
