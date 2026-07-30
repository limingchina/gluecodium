

from smoke.StructsAnotherExternalStruct import StructsAnotherExternalStruct
from smoke.StructsExternalStruct import StructsExternalStruct
import typing

class Structs:

    @staticmethod
    def get_external_struct() -> StructsExternalStruct:
        ...

    @staticmethod
    def get_another_external_struct() -> StructsAnotherExternalStruct:
        ...

