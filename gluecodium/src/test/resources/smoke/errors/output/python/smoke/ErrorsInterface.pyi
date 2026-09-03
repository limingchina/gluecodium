

from smoke.Payload import Payload
from smoke.WithPayloadError import WithPayloadError
from enum import Enum
import typing

class ErrorsInterface:

    def method_with_errors(self):
        ...

    def method_with_external_errors(self):
        ...

    def method_with_errors_and_return_value(self) -> str:
        ...

    @staticmethod
    def method_with_payload_error():
        ...

    @staticmethod
    def method_with_payload_error_and_return_value() -> str:
        ...

    class InternalError(Enum):
    
        ERROR_NONE = 0
        ERROR_FATAL = 1
    
    
    
    class ExternalErrors(Enum):
    
        NONE = 0
        BOOM = 1
        BUST = 2
    
    
    
    class InternalError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    
    
    class ExternalError(Exception):
        message: str
    
        def __init__(self, message: str) -> None: ...
    
    

    ERROR_MESSAGE = "Some error message constant"

