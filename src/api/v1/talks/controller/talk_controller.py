from django.http import HttpRequest

from api.v1.base.base_controller import BaseController


class TalkController(BaseController):

    def get(self, request: HttpRequest):
        print('TalkController : ' + request.path)

        return self._getJsonResponse({
            'isSuccess': True
        })

    def post(self, request: HttpRequest):
        print('TalkController : ' + request.path)

        return self._getJsonResponse({
            'isSuccess': True
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
