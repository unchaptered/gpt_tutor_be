import uuid


class UuidProvider():

    def getUuidV4(self) -> str:
        return uuid.uuid4().__str__()
