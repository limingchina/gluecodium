

from smoke.ErrorsExternal import ErrorsExternal
from smoke.ErrorsExternalErrors import ErrorsExternalErrors
from smoke.ErrorsInternal import ErrorsInternal
from smoke.ErrorsInternalErrorCode import ErrorsInternalErrorCode
from smoke.Payload import Payload
from smoke.WithPayloadError import WithPayloadError
import typing

class Errors:

    @staticmethod
    def method_with_errors():
        ...

    @staticmethod
    def method_with_external_errors():
        ...

    @staticmethod
    def method_with_errors_and_return_value() -> str:
        ...

    @staticmethod
    def method_with_payload_error():
        ...

    @staticmethod
    def method_with_payload_error_and_return_value() -> str:
        ...

