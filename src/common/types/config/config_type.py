from typing import TypedDict


class OpenaiConfigType(TypedDict):
    API_KEY: str


class ConfigType(TypedDict):
    OPENAI: OpenaiConfigType
