from typing import TypedDict, Literal, List, Union


class GptCompletionUsageType(TypedDict):
    completion_tokens: int
    prompt_tokens: int
    total_tokens: int


class GptCompletionChoiceMessageType(TypedDict):
    content: str
    role: str


class GptCompletionChoiceType(TypedDict):
    finish_reason: str
    index: int
    message: GptCompletionChoiceMessageType


class GptCompletionResponseType(TypedDict):

    id: str
    created: int
    model: Union[Literal['gpt-3.5-turbo-0613'], str]
    object: str
    usage: GptCompletionUsageType
    choices: List[GptCompletionChoiceType]
