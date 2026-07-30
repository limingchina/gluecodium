

from smoke.ExternalClassConstructorExploded import ExternalClassConstructorExploded
from smoke.ExternalClassErrorEnum import ExternalClassErrorEnum
import typing

class ExternalClassInternalOne:

    @staticmethod
    def create() -> ExternalClassInternalOne:
        ...

    @staticmethod
    def create(value: int) -> ExternalClassInternalOne:
        ...

