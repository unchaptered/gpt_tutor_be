from typing import TypedDict


class OpenaiConfigType(TypedDict):
    API_KEY: str


class RdsConfigType(TypedDict):
    HOST: str
    PORT: int
    USER: str
    PWD: str
    DB_NAME: str
    DB_CONNECTION_LIMIT: int


class SqsConfigType(TypedDict):
    QUEUE_URL: str
    REGION_NAME: str
    ACCESS_KEY: str
    SECRET_ACCESS_KEY: str


class ConfigType(TypedDict):
    OPENAI: OpenaiConfigType
    RDS: RdsConfigType
    SQS: SqsConfigType
