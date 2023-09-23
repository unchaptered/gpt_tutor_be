from typing import Literal, List
import re
import tiktoken
import openai
import requests
import json

from enum import Enum

# commons
from common.enums.gpt.e_gpt_role import EGPT_ROLE
from common.enums.gpt.e_gpt_instrucments import EGPT_INSTURMENTS
from common.types.gpt.gpt_completion_type import GptCompletionResponseType
from common.enums.talk.e_talk_status import ETALK_STATUS

# aws
from aws.sqs_provider import SqsProvider

# gpt
from gpt.gpt_message import GptMessage, GptMessageList

# utilities
from utilities.config_provider import configProvider

# layers
from api.v1.chats.service.chat_service import ChatService
from api.v1.talks.service.talk_service import TalkService

openai.api_key = configProvider.getConfig()['OPENAI']['API_KEY']

class GptCore():
    
    __sqsProvider: SqsProvider
    
    __chatService: ChatService
    __talkService: TalkService
    
    def __init__(self) -> None:
        self.__sqsProvider = SqsProvider()
        
        self.__chatService = ChatService()
        self.__talkService = TalkService()
    
    def run(self):
        message = self.__sqsProvider.getMessage('sampleGroup')
        if message is None:
            return print('현재 질문 대상이 존재하지 않습니다.')
        
        sendMessage = message['body']
        print(sendMessage)
        
        try:
            
            # RECEIVED_FROM_QUEUE(UNUSED!!!) # (LEGACY)
            chatData = self.__chatService.getChatMetaDataForGPT(sendMessage)
            talkData = self.__talkService.getTalkMetaDataForGPT(sendMessage)
            
            # Conditional Actions
            isEndedChat = chatData['isEnded'] == 1
            isProblemSolvedChat = chatData['isProblemSolved'] == 1
            isAnsweredTalk = talkData['isAnswered'] == 1
            bannedTalkStatusList: List[str] = [
                ETALK_STATUS.BE_CANCEL.value,
                ETALK_STATUS.NON_PEDING.value,
                ETALK_STATUS.OVER_PENDING.value,
                
                ETALK_STATUS.CALL_GPT.value,
                ETALK_STATUS.SUCCESS_GPT.value,
                ETALK_STATUS.FAILURE_GPT.value
            ]
            isBannedTalkStatus = talkData['talkStatus'] in bannedTalkStatusList
            
            print(chatData)
            print(talkData)
            
            print('isEndedChat : ', isEndedChat)
            print('isProblemSolvedChat : ', isProblemSolvedChat)
            print('isAnsweredTalk : ', isAnsweredTalk)
            print('isBannedTalkStatus : ', isBannedTalkStatus)
            
            if (isEndedChat
                or isProblemSolvedChat
                or isAnsweredTalk
                or isBannedTalkStatus):
                raise ValueError('Conditional Actions Validation Failed : invalid gpt target')
            
            self.__talkService.patchTalkStatusForGPT(sendMessage=sendMessage,
                                                     TALK_STATUS=ETALK_STATUS.CALL_GPT)
            try:
                
                category = chatData['category']
                allowedList: List[str] = [ 'JAVA', 'JAVASCRIPT', 'KOTLIN', 'REACT', 'NEXT_JS', 'NODE_JS', 'NEST_JS', 'SPRING', 'CS' ]
                
                GPT_INSTURMENTS: EGPT_INSTURMENTS
                if category in allowedList:
                    GPT_INSTURMENTS = EGPT_INSTURMENTS[category]
                else:
                    GPT_INSTURMENTS = EGPT_INSTURMENTS.ETC
                    
                gptMessageList = GptMessageList()
                gptMessageList.appendGptInstrucments(GPT_INSTURMENTS)
                gptMessageList.appendGptMessage(GptMessage(
                    role=EGPT_ROLE.USER,
                    content=talkData['talkContext']
                ))
                gptResponse = self.completion(gptMessageList)
                gptAnswer = self.__convertGptChociesToStr(gptResponse)
                print(gptAnswer)
                print(type(gptAnswer))
                
                self.__talkService.patchTalkAnswerForGPT(sendMessage=sendMessage,
                                                        asnwer=gptAnswer)
            except Exception as e:
                print('112 line')
                print(e)
                self.__talkService.patchTalkStatusForGPT(sendMessage=sendMessage,
                                                        TALK_STATUS=ETALK_STATUS.FAILURE_GPT)
                # self.__sqsProvider.delMessage(message['receiptHandle'])
                
        except Exception as e:
            print('119 line')
            print(e)
            # self.__sqsProvider.delMessage(message['receiptHandle'])
            
        finally:
            self.__sqsProvider.delMessage(message['receiptHandle'])
            
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

    def __convertUnicodeToStr(self, match):
        return chr(int(match.group(1), 16))
    
    def __convertGptChociesToStr(self,
                                 response: GptCompletionResponseType):
        validStrList = []
        for choice in response['choices']:
            unicodeEscape = choice['message']['content']
            validStr = re.sub(r'\\u([a-fA-F0-9]{4})', self.__convertUnicodeToStr, unicodeEscape)
            validStrList.append(validStr)
        
        return '\n'.join(validStrList)


if __name__ == '__main__':

    gptMsgs = GptMessageList()
    gptMsgs.appendGptInstrucments(EGPT_INSTURMENTS.NODE_JS)
    gptMsgs.appendGptMessage(GptMessage(
        role=EGPT_ROLE.USER,
        content='Do you know react?'))
    format = gptMsgs.getCvtedGptFormat()
