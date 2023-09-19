from enum import Enum

class EGPT_ROLE(Enum):

    # 대화의 초기 설정 및 지시사항
    # 대화의 맥락을 설정하거나 특별한 규칙을 지정
    SYSTEM = 'system'

    # 요청자가 질문자(user)의 역할을 수행
    USER = 'user'

    # 요청자가 대답자(assistant)의 역할을 수행
    ASSISTANT = 'assistant'
