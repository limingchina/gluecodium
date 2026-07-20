

from smoke.ErrorsExternalErrors import ErrorsExternalErrors
from smoke.ErrorsInternalErrorCode import ErrorsInternalErrorCode
from smoke.Payload import Payload
import typing

from _native_base import _NativeBase

import generated


class Errors(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def method_with_errors(): ...

    @staticmethod
    def method_with_external_errors(): ...

    @staticmethod
    def method_with_errors_and_return_value() -> str: ...

    @staticmethod
    def method_with_payload_error(): ...

    @staticmethod
    def method_with_payload_error_and_return_value() -> str: ...

