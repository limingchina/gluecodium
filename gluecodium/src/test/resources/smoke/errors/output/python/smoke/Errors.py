

from __future__ import annotations

from smoke.ErrorsExternal import ErrorsExternal
from smoke.ErrorsExternalErrors import ErrorsExternalErrors
from smoke.ErrorsInternal import ErrorsInternal
from smoke.ErrorsInternalErrorCode import ErrorsInternalErrorCode
from smoke.Payload import Payload
from smoke.WithPayloadError import WithPayloadError

from _native_base import _NativeBase

import generated


class Errors(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_errors():
        """"""
        generated.Errors.method_with_errors()

    @staticmethod
    def method_with_external_errors():
        """"""
        generated.Errors.method_with_external_errors()

    @staticmethod
    def method_with_errors_and_return_value() -> str:
        """"""
        return generated.Errors.method_with_errors_and_return_value()

    @staticmethod
    def method_with_payload_error():
        """"""
        generated.Errors.method_with_payload_error()

    @staticmethod
    def method_with_payload_error_and_return_value() -> str:
        """"""
        return generated.Errors.method_with_payload_error_and_return_value()

