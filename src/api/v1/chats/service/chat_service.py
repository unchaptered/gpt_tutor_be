# modules
from utilities.uuid_provider import UuidProvider
from utilities.date_provider import DateProvider

# layers
from api.v1.base.base_service import BaseService
from api.v1.chats.repository.chat_repository import ChatRepository


class ChatService(BaseService):

    def __init__(self) -> None:
        super().__init__()

        # modules
        self.__uuidProvider = UuidProvider()
        self.__dateProvider = DateProvider()

        # layers
        self.__chatRepository = ChatRepository()

    def getAllChats(self, hostKey: str):

        with self._rdsProvider.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)

            chats = self.__chatRepository.getAllChats(cursor, hostKey)

            cursor.close()
            conn.commit()

            return chats

    def postChat(self, hostKey: str) -> str:

        with self._rdsProvider.get_connection() as conn:
            cursor = conn.cursor(dictionary=True)

            chatUuid = self.__uuidProvider.getUuidV4()
            currDatetime = self.__dateProvider.getCurrDatetimeStr()
            self.__chatRepository.postChats(cursor=cursor,
                                            hostKey=hostKey,
                                            chatUuid=chatUuid,
                                            currDatetime=currDatetime)

            cursor.close()
            conn.commit()

            return chatUuid