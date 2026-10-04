

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase, _install_callback_adapters, _unwrap_struct_args, _mark_callback_base
from enum import Enum
from typing import Optional
import generated

from smoke.Payload import Payload
from smoke.WithPayloadError import WithPayloadError

@_mark_callback_base
class ErrorsInterface(generated.smoke_ErrorsInterface):
    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        _install_callback_adapters(cls, __class__, [
            ("method_with_errors", "__gluecodium_callback_736d6f6b652e4572726f7273496e746572666163652e6d6574686f64576974684572726f7273", "method", None,
             lambda: ([], None)),
            ("method_with_external_errors", "__gluecodium_callback_736d6f6b652e4572726f7273496e746572666163652e6d6574686f645769746845787465726e616c4572726f7273", "method", None,
             lambda: ([], None)),
            ("method_with_errors_and_return_value", "__gluecodium_callback_736d6f6b652e4572726f7273496e746572666163652e6d6574686f64576974684572726f7273416e6452657475726e56616c7565", "method", None,
             lambda: ([], str)),
        ])
    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor and retain the original native object for calls back into
        # C++; otherwise construct a fresh trampoline.
        if native is not None and isinstance(native, generated.smoke_ErrorsInterface):
            super().__init__(native)
            self._native = native
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
        return _wrap(generated.smoke_ErrorsInterface.method_with_payload_error_and_return_value(), str)

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

