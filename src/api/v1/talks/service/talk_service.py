# commons
from common.enums.gpt.e_gpt_role import EGPT_ROLE
from common.enums.gpt.e_gpt_instrucments import EGPT_INSTURMENTS
from common.types.gpt.gpt_completion_type import GptCompletionResponseType

from common.enums.talk.e_talk_status import ETALK_STATUS
# gpt # (LEGACY)
# from gpt.gpt_core import GptCore # (LEGACY)
# from gpt.gpt_message import GptMessage, GptMessageList # (LEGACY)

# aws
from aws.sqs_provider import SqsProvider, SendMessageType

# modules
from utilities.uuid_provider import UuidProvider
from utilities.date_provider import DateProvider

# layers
from api.v1.base.base_service import BaseService
from api.v1.talks.repository.talk_repository import TalkRepository


class TalkService(BaseService):

    __sqsProvider: SqsProvider
    
    # __gptCore: GptCore # (LEGACY)
    
    __uuidProvider: UuidProvider
    __dateProvider: DateProvider
    
    __sqsProvider: SqsProvider
    
    __talkRepository: TalkRepository

    def __init__(self) -> None:
        super().__init__()
        
        # aws
        self.__sqsProvider = SqsProvider()
        
        # gpt
        # self.__gptCore = GptCore() # (LEGACY)
        
        # modules
        self.__uuidProvider = UuidProvider()
        self.__dateProvider = DateProvider()
        
        self.__sqsProvider = SqsProvider()
            
        # layers
        self.__talkRepository = TalkRepository()
    
    # Logics
    
    def getTalk(self,
                chatUuid: str,
                talkUuid: str):
        
        with self._rdsProvider.getConnection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.close()
            self.__sqsProvider.getMessage(
                groupId='sampleGroup'
            )
            
            conn.commit()
    
    def postTalk(self,
                chatUuid: str,
                context: str):
        
        with self._rdsProvider.getConnection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            talkUuid = self.__uuidProvider.getUuidV4()
            currDatetimeStr = self.__dateProvider.getCurrDatetimeStr()
            self.__talkRepository.postTalk(cursor=cursor,
                                           chatUuid=chatUuid,
                                           talkUuid=talkUuid,
                                           context=context,
                                           createdAt=currDatetimeStr,
                                           TALK_STATUS=ETALK_STATUS.REGISTERED_INTO_QUEUE)
            isPosted = self.__sqsProvider.postMessage(
                groupId='sampleGroup',
                groupMessage={
                    'chatUuid': chatUuid,
                    'talkUuid': talkUuid
                }
            )
            # if not isPosted: # (LEGACY)
            # if True:
            #     raise RuntimeError('SQS 메세지 등록에 실패하였습니다.')
            
            cursor.close()
            conn.commit()
            
            return talkUuid

    # for APScheudler/GPT
    
    def getTalkMetaDataForGPT(self,
                      sendMessage: SendMessageType):

        with self._rdsProvider.getConnection() as conn:
            cursor = conn.cursor(dictionary=True)
            talkData = self.__talkRepository.getTalkMetaDataForGPT(cursor=cursor,
                                                        sendMessage=sendMessage)
            
            cursor.close()
            conn.commit()
            
            return talkData
    
    def patchTalkStatusForGPT(self,
                      sendMessage: SendMessageType,
                      TALK_STATUS: ETALK_STATUS):

        with self._rdsProvider.getConnection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            updatedAt = self.__dateProvider.getCurrDatetimeStr()
            talkData = self.__talkRepository.patchTalkStatus(cursor=cursor,
                                                        chatUuid=sendMessage['chatUuid'],
                                                        talkUuid=sendMessage['talkUuid'],
                                                        updatedAt=updatedAt,
                                                        TALK_STATUS=TALK_STATUS)
            
            cursor.close()
            conn.commit()
            
            return talkData
        
    def patchTalkAnswerForGPT(self,
                      sendMessage: SendMessageType,
                      asnwer: str):

        with self._rdsProvider.getConnection() as conn:
            cursor = conn.cursor(dictionary=True)
            
            answeredAt = self.__dateProvider.getCurrDatetimeStr()
            talkData = self.__talkRepository.patchTalkAsnwer(cursor=cursor,
                                                        chatUuid=sendMessage['chatUuid'],
                                                        talkUuid=sendMessage['talkUuid'],
                                                        answer=asnwer,
                                                        answeredAt=answeredAt,
                                                        TALK_STATUS=ETALK_STATUS.SUCCESS_GPT)
            
            cursor.close()
            conn.commit()
            
            return talkData
    
    
    # def sendQuestion(self, chatUuid: str, context: str): # (LEGACY)

    #     gptList = GptMessageList()
    #     gptList.appendGptInstrucments(EGPT_INSTURMENTS.JAVA)
    #     gptList.appendGptMessage(GptMessage(
    #         role=EGPT_ROLE.USER,
    #         content=context
    #     ))

    #     isValid = self.__gptCore.isValidMsg(
    #         gptList, model='gpt-3.5-turbo-0613')

    #     if isValid:
    #         response = self.__gptCore.completion(gptList)
    #         print(response)
    #         return response['choices'][0]['message']

    #     return 'is not valid tokens'
