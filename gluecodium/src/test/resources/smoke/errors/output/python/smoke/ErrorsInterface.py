

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.ErrorsInterfaceExternal import ErrorsInterfaceExternal
from smoke.ErrorsInterfaceExternalErrors import ErrorsInterfaceExternalErrors
from smoke.ErrorsInterfaceInternal import ErrorsInterfaceInternal
from smoke.ErrorsInterfaceInternalError import ErrorsInterfaceInternalError
from smoke.Payload import Payload
from smoke.WithPayloadError import WithPayloadError


import generated


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

    ERROR_MESSAGE = "Some error message constant"

