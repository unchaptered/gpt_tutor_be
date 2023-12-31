from typing import List, Literal, Optional, TypedDict
from mysql.connector.cursor import MySQLCursor

# commons
from common.enums.talk.e_talk_status import ETALK_STATUS

# aws
from aws.sqs_provider import SendMessageType

class TalkPacketType(TypedDict):
    hostKey: str
    chatUuid: str
    createdAt: str
    
class TalkGptPacketType(TypedDict):
    chatUuid: str
    talkUuid: str
    talkContext: str
    talkStatus: str
    isAnswered: Literal[1, 0]
    
class TalkResponsePacketType(TypedDict):
    chatUuid:str
    talkUuid: str
    talkContext: str
    talkStatus: str
    createdAt: str
    updatedAt: str
    answeredAt: str
    isAnswered: Literal[1, 0]
    answerContext: str

class TalkRepository():

    def getTalk(self,
                cursor: MySQLCursor,
                chatUuid: str) -> List[TalkResponsePacketType]:
        cursor.execute(f"""
            SELECT  chat_uuid as chatUuid,
                    talk_uuid as talkUuid,
                    talk_context as talkContext,
                    talk_status as talkStatus,
                    created_at as createdAt,
                    updated_at as updatedAt,
                    answered_at as answeredAt,
                    is_answered as isAnswered,
                    answer_context as answerContext
            FROM    talk
            WHERE   chat_uuid = '{chatUuid}'
            ORDER BY created_at ASC;
        """)
        result: List[TalkResponsePacketType] = cursor.fetchall() # type: ignore
        return result
    
    def getSingleTalk(self,
                cursor: MySQLCursor,
                chatUuid: str,
                talkUuid: str) -> TalkResponsePacketType:
        cursor.execute(f"""
            SELECT  chat_uuid as chatUuid,
                    talk_uuid as talkUuid,
                    talk_context as talkContext,
                    talk_status as talkStatus,
                    created_at as createdAt,
                    updated_at as updatedAt,
                    answered_at as answeredAt,
                    is_answered as isAnswered,
                    answer_context as answerContext
            FROM    talk
            WHERE   chat_uuid = '{chatUuid}'
            AND     talk_uuid = '{talkUuid}';
        """)
        result: Optional[TalkResponsePacketType] = cursor.fetchone() # type: ignore
        if result is None:
            raise ValueError('존재하지 않는 토크')
        
        return result

    def postTalk(self,
                cursor: MySQLCursor,
                chatUuid: str,
                talkUuid: str,
                context: str,
                createdAt: str,
                TALK_STATUS: ETALK_STATUS):
        cursor.execute(f"""
            INSERT INTO talk (
                chat_uuid,      talk_uuid,      created_at,
                talk_context,   talk_status
            ) VALUES (
                '{chatUuid}',   '{talkUuid}',   '{createdAt}',
                '{context}',    '{TALK_STATUS.value}'
            );
        """)
        
    def patchTalkStatus(self,
                        cursor: MySQLCursor,
                        chatUuid: str,
                        talkUuid: str,
                        updatedAt: str,
                        TALK_STATUS: ETALK_STATUS):
        cursor.execute(f"""
            UPDATE  talk
            SET     talk_status = '{TALK_STATUS.value}',
                    updated_at = '{updatedAt}'
            WHERE   chat_uuid = '{chatUuid}'
            AND     talk_uuid = '{talkUuid}';
        """)
        
    def patchTalkAsnwer(self,
                        cursor: MySQLCursor,
                        chatUuid: str,
                        talkUuid: str,
                        answeredAt: str,
                        answer: str,
                        TALK_STATUS: ETALK_STATUS):
        cursor.execute(f"""
            UPDATE  talk
            SET     talk_status = '{TALK_STATUS.value}',
                    answered_at = '{answeredAt}',
                    answer_context = '{answer}'
            WHERE   chat_uuid = '{chatUuid}'
            AND     talk_uuid = '{talkUuid}';
        """)
        
    def getTalkMetaDataForGPT(self,
                              cursor: MySQLCursor,
                              sendMessage: SendMessageType) -> TalkGptPacketType:
        cursor.execute(f"""
            SELECT  chat_uuid as chatUuid,
                    talk_uuid as talkUuid,
                    talk_context as talkContext,
                    talk_status as talkStatus,
                    is_answered as isAnswered
            FROM    talk
            WHERE   chat_uuid = '{sendMessage['chatUuid']}'
            AND     talk_uuid = '{sendMessage['talkUuid']}'
            LIMIT   1;
        """)
        result: Optional[TalkGptPacketType] = cursor.fetchone()  # type: ignore
        if result is None:
            raise ValueError('getTalkMetaDataForGPT cannot find target talk')
        
        return result