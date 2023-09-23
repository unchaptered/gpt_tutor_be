from aws.sqs_provider import SendMessageType

# modules
from utilities.uuid_provider import UuidProvider
from utilities.date_provider import DateProvider


# layers
from api.v1.base.base_service import BaseService
from api.v1.chats.repository.chat_repository import ChatRepository


class ChatService(BaseService):

    __uuidProvider: UuidProvider
    __dateProvider: DateProvider

    __chatRepository: ChatRepository

    def __init__(self) -> None:
        super().__init__()

        # modules
        self.__uuidProvider = UuidProvider()
        self.__dateProvider = DateProvider()

        # layers
        self.__chatRepository = ChatRepository()
        
    # for layers

    def getAllChats(self, hostKey: str):

        with self._rdsProvider.getConnection() as conn:
            cursor = conn.cursor(dictionary=True)

            chats = self.__chatRepository.getAllChats(cursor, hostKey)

            cursor.close()
            conn.commit()

            return chats

    def postChat(self, hostKey: str, category: str) -> str:

        with self._rdsProvider.getConnection() as conn:
            cursor = conn.cursor(dictionary=True)

            chatUuid = self.__uuidProvider.getUuidV4()
            currDatetime = self.__dateProvider.getCurrDatetimeStr()
            self.__chatRepository.postChats(cursor=cursor,
                                            hostKey=hostKey,
                                            chatUuid=chatUuid,
                                            category=category,
                                            currDatetime=currDatetime)

            cursor.close()
            conn.commit()

            return chatUuid

    def getChatByUuid(self, hostKey: str, chatUuid: str):

        with self._rdsProvider.getConnection() as conn:
            cursor = conn.cursor(dictionary=True)

            chat = self.__chatRepository.getChatByUuid(cursor=cursor,
                                                       hostKey=hostKey,
                                                       chatUuid=chatUuid)

            cursor.close()
            conn.commit()

            return chat

    def delChatByUuid(self, hostKey: str, chatUuid: str):

        with self._rdsProvider.getConnection() as conn:
            cursor = conn.cursor(dictionary=True)

            chat = self.__chatRepository.delChatByUuid(cursor=cursor,
                                                       hostKey=hostKey,
                                                       chatUuid=chatUuid)

            cursor.close()
            conn.commit()

            return chat

    # for APScheudler/GPT
    
    def getChatMetaDataForGPT(self,
                      sendMessage: SendMessageType):

        with self._rdsProvider.getConnection() as conn:
            cursor = conn.cursor(dictionary=True)
            chatData = self.__chatRepository.getChatMetaDataForGPT(cursor=cursor,
                                                        sendMessage=sendMessage)
            
            cursor.close()
            conn.commit()
            return chatData