

from smoke.ExternalClassConstructorExploded import ExternalClassConstructorExploded
from smoke.ExternalClassErrorEnum import ExternalClassErrorEnum
from smoke.ExternalClassInternalOne import ExternalClassInternalOne
from smoke.ExternalClassInternalTwo import ExternalClassInternalTwo
import typing

class ExternalClass:

    @staticmethod
    def create() -> ExternalClass:
        ...

