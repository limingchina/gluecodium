

from smoke.ErrorsInterfaceExternal import ErrorsInterfaceExternal
from smoke.ErrorsInterfaceExternalErrors import ErrorsInterfaceExternalErrors
from smoke.ErrorsInterfaceInternal import ErrorsInterfaceInternal
from smoke.ErrorsInterfaceInternalError import ErrorsInterfaceInternalError
from smoke.Payload import Payload
from smoke.WithPayloadError import WithPayloadError
import typing

class ErrorsInterface:

    def method_with_errors(self):
        ...

    def method_with_external_errors(self):
        ...

    def method_with_errors_and_return_value(self) -> str:
        ...

    @staticmethod
    def method_with_payload_error():
        ...

    @staticmethod
    def method_with_payload_error_and_return_value() -> str:
        ...

    ERROR_MESSAGE = "Some error message constant"

