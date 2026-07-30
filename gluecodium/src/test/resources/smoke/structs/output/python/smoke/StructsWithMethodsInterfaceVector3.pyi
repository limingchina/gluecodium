

from smoke.ValidationUtilsValidation import ValidationUtilsValidation
from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode
import typing

class StructsWithMethodsInterfaceVector3:

    x: float

    y: float

    z: float

    def distance_to(self, other: StructsWithMethodsInterfaceVector3) -> float:
        ...

    def add(self, other: StructsWithMethodsInterfaceVector3) -> StructsWithMethodsInterfaceVector3:
        ...

    @staticmethod
    def validate(x: float, y: float, z: float) -> bool:
        ...

    @staticmethod
    def create(input: str) -> StructsWithMethodsInterfaceVector3:
        ...

    @staticmethod
    def create(other: StructsWithMethodsInterfaceVector3) -> StructsWithMethodsInterfaceVector3:
        ...

