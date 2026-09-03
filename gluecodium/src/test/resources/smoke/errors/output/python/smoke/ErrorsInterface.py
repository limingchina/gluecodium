

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.Payload import Payload
from smoke.WithPayloadError import WithPayloadError

class ErrorsInterface(generated.smoke_ErrorsInterface):
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_ErrorsInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    def method_with_errors(self):
        return _wrap(generated.smoke_ErrorsInterface.method_with_errors(self), None)

    def method_with_external_errors(self):
        return _wrap(generated.smoke_ErrorsInterface.method_with_external_errors(self), None)

    def method_with_errors_and_return_value(self) -> str:
        return _wrap(generated.smoke_ErrorsInterface.method_with_errors_and_return_value(self), str)

    @staticmethod
    def method_with_payload_error():
        generated.smoke_ErrorsInterface.method_with_payload_error()

    @staticmethod
    def method_with_payload_error_and_return_value() -> str:
        return generated.smoke_ErrorsInterface.method_with_payload_error_and_return_value()

    class InternalError(Enum):
    
        ERROR_NONE = generated.smoke_ErrorsInterface.InternalError.ERROR_NONE
        ERROR_FATAL = generated.smoke_ErrorsInterface.InternalError.ERROR_FATAL
    
        @property
        def _native(self):
            return self.value
    
    
    
    class ExternalErrors(Enum):
    
        NONE = generated.smoke_ErrorsInterface.ExternalErrors.NONE
        BOOM = generated.smoke_ErrorsInterface.ExternalErrors.BOOM
        BUST = generated.smoke_ErrorsInterface.ExternalErrors.BUST
    
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
    
    

    ERROR_MESSAGE = "Some error message constant"

