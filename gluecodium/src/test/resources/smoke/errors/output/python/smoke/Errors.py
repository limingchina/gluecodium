

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.Payload import Payload
from smoke.WithPayloadError import WithPayloadError

class Errors(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_errors():
        generated.smoke_Errors.method_with_errors()

    @staticmethod
    def method_with_external_errors():
        generated.smoke_Errors.method_with_external_errors()

    @staticmethod
    def method_with_errors_and_return_value() -> str:
        return generated.smoke_Errors.method_with_errors_and_return_value()

    @staticmethod
    def method_with_payload_error():
        generated.smoke_Errors.method_with_payload_error()

    @staticmethod
    def method_with_payload_error_and_return_value() -> str:
        return generated.smoke_Errors.method_with_payload_error_and_return_value()

    class InternalErrorCode(Enum):
    
        ERROR_NONE = generated.smoke_Errors.InternalErrorCode.ERROR_NONE
        ERROR_FATAL = generated.smoke_Errors.InternalErrorCode.ERROR_FATAL
    
        @property
        def _native(self):
            return self.value
    
    
    
    class ExternalErrors(Enum):
    
        NONE = generated.smoke_Errors.ExternalErrors.NONE
        BOOM = generated.smoke_Errors.ExternalErrors.BOOM
        BUST = generated.smoke_Errors.ExternalErrors.BUST
    
        @property
        def _native(self):
            return self.value
    
    
    
    class InternalError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    
    
    class ExternalError(Exception):
    
        def __init__(self, message: str):
            super().__init__(message)
            self.message = message
    
    

