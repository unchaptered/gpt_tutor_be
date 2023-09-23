from typing import List, Optional, TypedDict, Literal
from mysql.connector.cursor import MySQLCursor

# sqs
from aws.sqs_provider import SendMessageType

class ChatPacketType(TypedDict):
    hostKey: str
    chatUuid: str
    createdAt: str
    
class ChatGptPacketType(TypedDict):
    hostKey: str
    chatUuid: str
    createdAt: str
    category: str
    isEnded: Literal[1, 0]
    isProblemSolved: Literal[1, 0]

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
        result: List[ChatPacketType] = cursor.fetchall() # type: ignore
        return result

    def postChats(self,
                  cursor: MySQLCursor,
                  hostKey: str,
                  chatUuid: str,
                  category: str,
                  currDatetime: str):
        cursor.execute(f"""
            INSERT INTO chat (
                host_key,       chat_uuid,
                category,       created_at
            ) VALUES
            (
                '{hostKey}',    '{chatUuid}',
                '{category}',   '{currDatetime}'
            );
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

        result: Optional[ChatPacketType] = cursor.fetchall() # type: ignore
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

    def getChatMetaDataForGPT(self,
                            cursor: MySQLCursor,
                            sendMessage: SendMessageType) -> ChatGptPacketType:
        cursor.execute(f"""
            SELECT
                    host_key as hostKey,
                    chat_uuid as chatUuid,
                    created_at as createdAt,
                    category as category,
                    is_ended as isEnded,
                    is_problem_solved as isProblemSolved
            FROM    chat
            WHERE   chat_uuid = '{sendMessage['chatUuid']}'
            LIMIT   1;
        """)
    
        result: Optional[ChatGptPacketType] = cursor.fetchone() # type: ignore
        if result is None:
            raise ValueError('getChatMetaDataForGPT result is none')
        
        return result
    