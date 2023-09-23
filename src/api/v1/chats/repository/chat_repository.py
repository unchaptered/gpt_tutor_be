from typing import List, Optional, TypedDict
from mysql.connector.cursor import MySQLCursor


class ChatPacketType(TypedDict):
    hostKey: str
    chatUuid: str
    createdAt: str


class ChatRepository():

    def getAllChats(self, cursor: MySQLCursor, hostKey: str) -> List[ChatPacketType]:
        cursor.execute(f"""
            SELECT
                host_key as hostKey,
                chat_uuid as chatUuid,
                created_at as createdAt
            FROM chat
            WHERE host_key = '{hostKey}';
        """)
        result: List[ChatPacketType] = cursor.fetchall()
        return result

    def postChats(self,
                  cursor: MySQLCursor,
                  hostKey: str,
                  chatUuid: str,
                  currDatetime: str):
        cursor.execute(f"""
            INSERT INTO chat (host_key, chat_uuid, created_at) VALUES
            ('{hostKey}', '{chatUuid}', '{currDatetime}');
        """)

    def getChatByUuid(self,
                      cursor: MySQLCursor,
                      hostKey: str,
                      chatUuid: str) -> ChatPacketType:
        cursor.execute(f"""
                       SELECT 
                            host_key as hostKey,
                            chat_uuid as chatUuid,
                            created_at as createdAt
                       FROM chat
                       WHERE host_key = '{hostKey}'
                       AND   chat_uuid = '{chatUuid}';
                       """)

        result: Optional[ChatPacketType] = cursor.fetchall()
        if result is None:
            raise ValueError('getChatByUuid result is none')

        return result

    def delChatByUuid(self,
                      cursor: MySQLCursor,
                      hostKey: str,
                      chatUuid: str):
        cursor.execute(f"""
                       DELETE FROM chat
                       WHERE host_key = '{hostKey}'
                       AND   chat_uuid = '{chatUuid}';
                       """)
