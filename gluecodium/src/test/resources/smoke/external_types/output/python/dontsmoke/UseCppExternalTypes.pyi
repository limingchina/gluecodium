

from smoke.ClassWithOverloads import ClassWithOverloads
from smoke.Enums import Enums
from smoke.Structs import Structs
from enum import Enum
import typing

class UseCppExternalTypes:

    @staticmethod
    def use_struct(input: Structs.AnotherExternalStruct):
        ...

    @staticmethod
    def use_enum(input: Enums.ExternalEnum):
        ...

    @staticmethod
    def use_class(input: ClassWithOverloads):
        ...


