from typing import List, Optional, TypedDict
from mysql.connector.cursor import MySQLCursor

# commons
from common.enums.talk.e_talk_status import ETALK_STATUS


class ChatPacketType(TypedDict):
    hostKey: str
    chatUuid: str
    createdAt: str


class TalkRepository():

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
            UPDATE talk
            SET     talk_status = '{TALK_STATUS.value}',
                    answered_at = '{answeredAt}',
                    answer = '{answer}'
            WHERE   chat_uuid = '{chatUuid}'
            AND     talk_uuid = '{talkUuid}';
        """)