from typing import Literal, List
import tiktoken
import openai
import requests
import json

from enum import Enum

# Types
from common.enums.gpt.e_gpt_role import EGPT_ROLE
from common.enums.gpt.e_gpt_instrucments import EGPT_INSTURMENTS
from common.types.gpt.gpt_completion_type import GptCompletionResponseType

# GPT
from gpt.gpt_message import GptMessage, GptMessageList

# Utility
from utilities.config_provider import configProvider

openai.api_key = configProvider.getConfig()['OPENAI']['API_KEY']


class GptCore():

    def completion(
        self,
        msgList: GptMessageList
    ) -> GptCompletionResponseType:
        response: GptCompletionResponseType = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=msgList.getCvtedGptFormat(),
            temperature=0
        )  # type: ignore

        return response

    def isValidMsg(
        self,
        messages: GptMessageList,
        model: Literal['gpt-3.5-turbo-0613'] = 'gpt-3.5-turbo-0613'
    ):
        if (self.__validateMsgToken(messages, model)
                and self.__validateMsgModeration(messages, model)):
            print('요청을 보내는 것이 합당합니다.')
            return True

        return False

    def __validateMsgToken(
        self,
        messages: GptMessageList,
        model: Literal['gpt-3.5-turbo-0613'] = 'gpt-3.5-turbo-0613'
    ) -> bool:
        tokenLength = self.__getMsgTokenCount(messages, model)
        return True if tokenLength <= 4096 else False

    def __validateMsgModeration(
        self,
        messages: GptMessageList,
        model: Literal['gpt-3.5-turbo-0613'] = 'gpt-3.5-turbo-0613'
    ) -> bool:

        # url = 'https://api.openai.com/v1/moderations'
        # api_key = ''
        # headers = {
        #     'Content-Type': 'application/json',
        #     'Authorization': f'Bearer {api_key}'
        # }

        # # 요청 본문 데이터
        # data = {
        #     "input": "Sample text goes here"
        # }

        # response = requests.post(url, headers=headers, json=data)
        # if response.status_code >= 400:

        #     print(response.status_code)
        #     print(response.json())

        # print('=' * 20)
        # print(response.status_code)
        # print(response.json())

        return True

    def __getMsgTokenCount(
        self,
        messages: GptMessageList,
        model: Literal['gpt-3.5-turbo-0613'] = 'gpt-3.5-turbo-0613'
    ):
        # Managing tokens : 토큰 관리
        # https://platform.openai.com/docs/guides/gpt/managing-tokens
        try:
            encoding = tiktoken.encoding_for_model(model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")

        cvtedMessages = messages.getCvtedGptFormat()

        if model == "gpt-3.5-turbo-0613":  # note: future models may deviate from this
            num_tokens = 0
            for message in cvtedMessages:
                # every message follows <im_start>{role/name}\n{content}<im_end>\n
                num_tokens += 4

                for key, value in message.items():
                    num_tokens += len(encoding.encode(value))
                    if key == "name":  # if there's a name, the role is omitted
                        num_tokens += -1  # role is always required and always 1 token
            num_tokens += 2  # every reply is primed with <im_start>assistant
            return num_tokens

        raise NotImplementedError(f"""
            num_tokens_from_messages() is not presently implemented for model {model}.
            See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens.
        """)


if __name__ == '__main__':

    gptMsgs = GptMessageList()
    gptMsgs.appendGptInstrucments(EGPT_INSTURMENTS.NODE_JS)
    gptMsgs.appendGptMessage(GptMessage(
        role=EGPT_ROLE.USER,
        content='Do you know react?'))
    format = gptMsgs.getCvtedGptFormat()
