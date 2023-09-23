from typing import List, TypedDict
from mysql.connector.cursor import MySQLCursor


class ChatPacketType(TypedDict):
    hostKey: str
    chatUuid: str
    createdAt: str


class ChatRepository():

    def getAllChats(self, cursor: MySQLCursor, hostKey: str):
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
