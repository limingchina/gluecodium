

from __future__ import annotations

from smoke.ExternalError import ExternalError
from smoke.ExternalErrors import ExternalErrors
from smoke.InternalError import InternalError
from smoke.InternalErrorCode import InternalErrorCode
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
        native_result = generated.Errors.method_with_errors()
        return None(native_result)

    @staticmethod

    def method_with_external_errors():
        """"""
        native_result = generated.Errors.method_with_external_errors()
        return None(native_result)

    @staticmethod

    def method_with_errors_and_return_value() -> str:
        """"""
        native_result = generated.Errors.method_with_errors_and_return_value()
        return str(native_result)

    @staticmethod

    def method_with_payload_error():
        """"""
        native_result = generated.Errors.method_with_payload_error()
        return None(native_result)

    @staticmethod

    def method_with_payload_error_and_return_value() -> str:
        """"""
        native_result = generated.Errors.method_with_payload_error_and_return_value()
        return str(native_result)

from enum import Enum


class InternalErrorCode(Enum):
    """"""

    ERROR_NONE = 0
    ERROR_FATAL = 1

from enum import Enum


class ExternalErrors(Enum):
    """"""

    NONE = 0
    BOOM = 1
    BUST = 2

