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


class ConfigType(TypedDict):
    OPENAI: OpenaiConfigType
    RDS: RdsConfigType
