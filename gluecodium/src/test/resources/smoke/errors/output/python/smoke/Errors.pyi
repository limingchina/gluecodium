

from smoke.ExternalError import ExternalError
from smoke.ExternalErrors import ExternalErrors
from smoke.InternalError import InternalError
from smoke.InternalErrorCode import InternalErrorCode
from smoke.Payload import Payload
from smoke.WithPayloadError import WithPayloadError

from _native_base import _NativeBase


class Errors(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    def method_with_errors(self):
        """"""
        return self._native.method_with_errors()


    def method_with_external_errors(self):
        """"""
        return self._native.method_with_external_errors()


    def method_with_errors_and_return_value(self) -> str:
        """"""
        return self._native.method_with_errors_and_return_value()


    def method_with_payload_error(self):
        """"""
        return self._native.method_with_payload_error()


    def method_with_payload_error_and_return_value(self) -> str:
        """"""
        return self._native.method_with_payload_error_and_return_value()

