import boto3
import json5
from typing import List, Literal, TypedDict, Optional
from mypy_boto3_sqs.type_defs import MessageTypeDef
from utilities.config_provider import configProvider

class SendMessageType(TypedDict):
    chatUuid: str
    talkUuid: str
    
class ReceiveMessageType(TypedDict):
    messageId: str
    receiptHandle: str
    mD5OfBody: str
    body: SendMessageType


class SqsProvider():

    def __init__(self) -> None:
        
        configInstance = configProvider.getConfig()
        self.__sqsUrl= configInstance['SQS']['QUEUE_URL']
        self.__sqsClient = boto3.client(service_name='sqs',
                    region_name=configInstance['SQS']['REGION_NAME'],
                    aws_access_key_id=configInstance['SQS']['ACCESS_KEY'],
                    aws_secret_access_key=configInstance['SQS']['SECRET_ACCESS_KEY']
        )
        
    def postMessage(self,
                    groupId: Literal['sampleGroup'],
                    groupMessage: SendMessageType) -> bool:
        
        jsonGroupMessage = json5.dumps(groupMessage)
        if jsonGroupMessage is None:
            return False
            
        response = self.__sqsClient.send_message(QueueUrl=self.__sqsUrl,
                                                MessageGroupId=groupId,
                                                MessageBody=jsonGroupMessage)
        responseMetaData = response['ResponseMetadata']
        if responseMetaData['HTTPStatusCode'] != 200:
            return False
        
        return True
        
    def getMessage(self,
                   groupId: Literal['sampleGroup']) -> Optional[ReceiveMessageType]:
        
        _3_SECONDS = 3
        response = self.__sqsClient.receive_message(QueueUrl=self.__sqsUrl,
                                         MaxNumberOfMessages=1,
                                         VisibilityTimeout=_3_SECONDS)
        responseMetaData = response['ResponseMetadata']
        isSuccessResponse = responseMetaData['HTTPStatusCode'] == 200
        if not isSuccessResponse:
            return None
        
        hasMessage = 'Messages' in response
        if not hasMessage:
            return None
        
        messageList = response['Messages']
        hasOneMessage = len(messageList) == 1
        if not hasOneMessage:
            return None
        
        return self.__convertMessage(messageTypeDef=messageList[0])
    
    def __convertSendMessageType(self,
                                body: str) -> SendMessageType:
        
        
        jsonMessageTypeBody = json5.loads(body)
        
        isDictType = type(jsonMessageTypeBody) is dict
        
        if not isDictType:
            raise TypeError('__convertSendMessageType 과정에서 에러 발생 : ' + str(jsonMessageTypeBody))
        
        hasChatUuid = 'chatUuid' in jsonMessageTypeBody
        hasTalkUuid = 'talkUuid' in jsonMessageTypeBody
        isValidSendMessageType = (hasChatUuid and hasTalkUuid)
        if not isValidSendMessageType:
            raise TypeError('__convertSendMessageType 과정에서 에러 발생(Key is not found) : ' + str(jsonMessageTypeBody))
        
        return {
            'chatUuid': jsonMessageTypeBody['chatUuid'],
            'talkUuid': jsonMessageTypeBody['talkUuid']
        }
        
    def __convertMessage(self,
                        messageTypeDef: MessageTypeDef) -> Optional[ReceiveMessageType]:
        
        isExistsMessageId = 'MessageId' in messageTypeDef
        isExistsReceiptHandle = 'ReceiptHandle' in messageTypeDef
        isExistsMD5OfBody = 'MD5OfBody' in messageTypeDef
        isExistsBody = 'Body' in messageTypeDef

        if (isExistsMessageId
            and isExistsReceiptHandle
            and isExistsMD5OfBody
            and isExistsBody):
            
            messageType: ReceiveMessageType = {
                'messageId': messageTypeDef['MessageId'],
                'receiptHandle': messageTypeDef['ReceiptHandle'],
                'mD5OfBody': messageTypeDef['MD5OfBody'],
                'body': self.__convertSendMessageType(messageTypeDef['Body'])
            }
            return messageType
                
    def __convertMessages(self,
                               messageTypeDefList: List[MessageTypeDef]) -> List[ReceiveMessageType]:
        messageTypeList = [
            self.__convertMessage(messageTypeDef)
            for messageTypeDef in messageTypeDefList
        ]
        validMessageTypeList = [
            messageType
            for messageType in messageTypeList
            if messageType is not None
        ]
        return validMessageTypeList
        