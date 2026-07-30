

from smoke.ClassWithOverloads import ClassWithOverloads
from smoke.EnumsExternal_Enum import EnumsExternal_Enum
from smoke.StructsAnotherExternalStruct import StructsAnotherExternalStruct
import typing

class UseCppExternalTypes:

    @staticmethod
    def use_struct(input: StructsAnotherExternalStruct):
        ...

    @staticmethod
    def use_enum(input: EnumsExternal_Enum):
        ...

    @staticmethod
    def use_class(input: ClassWithOverloads):
        ...

