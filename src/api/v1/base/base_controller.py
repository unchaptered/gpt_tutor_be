from django.views import View
from django.http import JsonResponse, HttpRequest
from json import loads

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Modules

from common.enums.e_status_code import ESTATUS_CODE

@method_decorator(csrf_exempt, name='dispatch')
class BaseController(View):

    def __init__(self):
        pass

    def _getRequestBody(
        self,
        bodyBytes: bytes
    ) -> dict:

        try:

            bodyStr = bodyBytes.decode('utf-8')
            bodyDict = loads(bodyStr)

            return bodyDict

        except Exception as e:
            return {}

    def _getJsonResponse(
        self,
        params: dict,
        statusCode: ESTATUS_CODE = ESTATUS_CODE.CREATED
    ):
        return JsonResponse(
            params,
            status=statusCode.value,
            json_dumps_params={'ensure_ascii': False}
        )

    def get(self, request: HttpRequest):
        print(request.path)
        
        return self._getJsonResponse({
            'isSuccess': True
        })

    def post(self, request: HttpRequest):
        print(request.path)
        
       
        return self._getJsonResponse({
            'isSuccess': True
        })

    def patch(self, request: HttpRequest):
        print(request.path)
        
       
        return self._getJsonResponse({
            'isSuccess': True
        })

    def put(self, request: HttpRequest):
        print(request.path)
        
       
        return self._getJsonResponse({
            'isSuccess': True
        })

    def delete(self, request: HttpRequest):
        print(request.path)
        
       
        return self._getJsonResponse({
            'isSuccess': True
        })
