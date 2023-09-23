from aws.rds_provider import RdsProvider


class BaseService():
    
    _rdsProvider: RdsProvider
    
    def __init__(self) -> None:        
        self._rdsProvider = RdsProvider()
