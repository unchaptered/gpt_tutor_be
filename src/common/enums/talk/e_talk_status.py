from enum import Enum

class ETALK_STATUS(Enum):
    """ETALK_STATUS

    Args:
        Enum (REGISTERED_INTO_QUEUE): 메세지가 큐에 등록됨
        
        Enum (RECEIVED_FROM_QUEUE): 메세지가 큐에서 불러와짐
        
        Enum (BE_CANCEL): 사용자가 수동으로 TALK Pulling을 취소함
        
        Enum (NON_PEDING): 일정 시간 마다 호출되는 TALK Pulling이 미호출됨
        
        Enum (OVER_PENDING): 일정 시간 마다 호출되는 TALK PUlling이 지정횟수 넘어감
        
        Enum (CALL_GPT): APScheduler에서 GPT 호출함
        
        Enum (SUCCESS_GPT): APScheduler에서 GPT 호출 결과가 성공함
        
        Enum (FAILRUE_GPT): APScheduler에서 GPT 호출 결과가 실패함
    """

    # QUQUE
    REGISTERED_INTO_QUEUE = 'REGISTERED_IN_QUEUE'
    """메세지가 큐에 등록됨"""
    
    RECEIVED_FROM_QUEUE = 'RECEIVED_IN_QUEUE'
    """메세지가 큐에서 불러와짐"""
    
    # INTERACTION
    
    BE_CANCEL = 'BE_CANCEL'
    """사용자가 수동으로 TALK Pulling을 취소함"""
    NON_PEDING = 'NON_PEDING'
    """일정 시간 마다 호출되는 TALK Pulling이 미호출됨"""
    OVER_PENDING = 'OVER_PENDING'
    """일정 시간 마다 호출되는 TALK PUlling이 지정횟수 넘어감"""
    
    # GPT
    
    CALL_GPT = 'CALL_GPT'
    """APScheduler에서 GPT 호출함"""
    SUCCESS_GPT = 'SUCCESS_GPT'
    """APScheduler에서 GPT 호출 결과가 성공함"""
    FAILURE_GPT = 'FAILURE_GPT'
    """APScheduler에서 GPT 호출 결과가 실패함"""