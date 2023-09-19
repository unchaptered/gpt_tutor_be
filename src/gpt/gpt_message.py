import json
from typing import List

# common
from common.enums.gpt.e_gpt_role import EGPT_ROLE
from common.enums.gpt.e_gpt_instrucments import EGPT_INSTURMENTS


class GptMessage():

    role: EGPT_ROLE
    content: str

    def __init__(self, role: EGPT_ROLE, content: str) -> None:
        self.role = role
        self.content = content

    def __str__(self) -> str:
        return '{ \"role\": \"' + self.role.value + '\", \"content\": \"' + self.content + '\" }'


class GptMessageList():

    gptMsgList: List[GptMessage] = []

    def __init__(self):
        pass

    def __str__(self) -> str:
        return '[' + ', '.join(str(gptMsg) for gptMsg in self.gptMsgList) + ']'

    def appendGptInstrucments(self, egpt_instrucments: EGPT_INSTURMENTS):
        self.gptMsgList.append(
            GptMessage(
                role=EGPT_ROLE.SYSTEM,
                content=egpt_instrucments.value
            )
        )

    def appendGptMessage(self, gptMessage: GptMessage) -> None:
        self.gptMsgList.append(gptMessage)

    def getCvtedGptFormat(self):
        return json.loads(self.__str__())
