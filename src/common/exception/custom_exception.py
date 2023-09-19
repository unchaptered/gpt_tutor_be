from typing import Optional, Literal, TypedDict, Any

# models
from common.enums.e_custom_exception_code import ECUSTOM_EXCEPTION_CODE


class CustomException(Exception):

    """
    메서드 전달 방식에 3가지가 있습니다.
    1. 일반 전달
    2. 키워드 전달 방식 (*)
    3. kwargs 전달 방식 (**)

    이 중에서 타입 안정성이 높고 기본값 할당에 용이한 키워드 전달 방식으로 에러를 확장해야 합니다.
    """

    statusCode: int

    errorCode: ECUSTOM_EXCEPTION_CODE

    errorPath: str
    errorMessage: str
    errorResponse: Optional[str]

    def __init__(self,
                 statusCode: int,
                 errorCode: ECUSTOM_EXCEPTION_CODE,
                 errorPath: str,
                 errorMessage: str,
                 errorResponse: Optional[str]) -> None:
        super().__init__()

        self.statusCode = statusCode
        self.errorCode = errorCode

        self.errorPath = errorPath
        self.errorMessage = errorMessage
        self.errorResponse = errorResponse

    def __str__(self):
        return f'{self.errorCode.value} {self.errorMessage}'


class SampleException(CustomException):

    """
    CustomException 주석 참고
    """
    statusCode: int

    errorCode: ECUSTOM_EXCEPTION_CODE

    errorPath: str
    errorMessage: str
    errorResponse: Optional[str]

    def __init__(self,
                 *,
                 statusCode: int = 500,
                 errorCode: ECUSTOM_EXCEPTION_CODE = ECUSTOM_EXCEPTION_CODE.SAMPLE_EXCEPTION,
                 errorPath: str = 'Converter',
                 errorMessage: str = '실행',
                 errorResponse: Optional[str] = None) -> None:

        super().__init__(statusCode, errorCode, errorPath, errorMessage, errorResponse)

        self.statusCode = statusCode
        self.errorCode = errorCode

        self.errorPath = errorPath
        self.errorMessage = errorMessage
        self.errorResponse = errorResponse
