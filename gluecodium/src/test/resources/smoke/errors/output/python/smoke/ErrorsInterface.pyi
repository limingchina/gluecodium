

from smoke.ExternalError import ExternalError
from smoke.ExternalErrors import ExternalErrors
from smoke.InternalError import InternalError
from smoke.Payload import Payload
from smoke.WithPayloadError import WithPayloadError


from _native_base import _NativeBase

import generated


class ErrorsInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ErrorsInterface):
            super().__init__(native)
        else:
            super().__init__(generated.ErrorsInterface())


    def method_with_errors(self):
        """"""
        return self._native.method_with_errors()


    def method_with_external_errors(self):
        """"""
        return self._native.method_with_external_errors()


    def method_with_errors_and_return_value(self) -> str:
        """"""
        return self._native.method_with_errors_and_return_value()

    @staticmethod

    def method_with_payload_error():
        """"""
        native_result = generated.ErrorsInterface.method_with_payload_error()
        return None(native_result)

    @staticmethod

    def method_with_payload_error_and_return_value() -> str:
        """"""
        native_result = generated.ErrorsInterface.method_with_payload_error_and_return_value()
        return str(native_result)

from enum import Enum


class InternalError(Enum):
    """"""

    ERROR_NONE = 0
    ERROR_FATAL = 1

from enum import Enum


class ExternalErrors(Enum):
    """"""

    NONE = 0
    BOOM = 1
    BUST = 2


ERROR_MESSAGE = "Some error message constant"

