from gpt.gpt_core import GptCore

class WorkHandler():
    
    __gptCore: GptCore
    def __init__(self) -> None:
        self.__gptCore = GptCore()

    def callGpt(self):
        self.__gptCore.run()

workHandler = WorkHandler()
