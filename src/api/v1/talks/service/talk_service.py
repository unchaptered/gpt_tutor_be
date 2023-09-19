# commons
from common.enums.gpt.e_gpt_role import EGPT_ROLE
from common.enums.gpt.e_gpt_instrucments import EGPT_INSTURMENTS

from common.types.gpt.gpt_completion_type import GptCompletionResponseType

# gpt
from gpt.gpt_core import GptCore
from gpt.gpt_message import GptMessage, GptMessageList


class TalkService():

    __gptCore: GptCore

    def __init__(self) -> None:
        self.__gptCore = GptCore()

    def sendQuestion(self, context: str):

        gptList = GptMessageList()
        gptList.appendGptInstrucments(EGPT_INSTURMENTS.JAVA)
        gptList.appendGptMessage(GptMessage(
            role=EGPT_ROLE.USER,
            content=context
        ))

        isValid = self.__gptCore.isValidMsg(
            gptList, model='gpt-3.5-turbo-0613')

        if isValid:
            response = self.__gptCore.completion(gptList)
            print(response)
            return response['choices'][0]['message']

        return 'is not valid tokens'
