

from smoke.ValidationUtilsValidation import ValidationUtilsValidation
from smoke.ValidationUtilsValidationErrorCode import ValidationUtilsValidationErrorCode
import typing

class StructsWithMethodsVector:

    x: float

    y: float

    def distance_to(self, other: StructsWithMethodsVector) -> float:
        ...

    def add(self, other: StructsWithMethodsVector) -> StructsWithMethodsVector:
        ...

    @staticmethod
    def validate(x: float, y: float) -> bool:
        ...

    @staticmethod
    def create(x: float, y: float) -> StructsWithMethodsVector:
        ...

    @staticmethod
    def create(other: StructsWithMethodsVector) -> StructsWithMethodsVector:
        ...

    @staticmethod
    def create(input: int) -> StructsWithMethodsVector:
        ...

