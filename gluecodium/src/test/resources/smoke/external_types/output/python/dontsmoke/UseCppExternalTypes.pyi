

from smoke.AnotherExternalStruct import AnotherExternalStruct
from smoke.ClassWithOverloads import ClassWithOverloads
from smoke.ExternalEnum import ExternalEnum


from _native_base import _NativeBase

import generated


class UseCppExternalTypes(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    @staticmethod

    def use_struct(input: AnotherExternalStruct):
        """"""
        native_result = generated.UseCppExternalTypes.use_struct(input)
        return None(native_result)

    @staticmethod

    def use_enum(input: ExternalEnum):
        """"""
        native_result = generated.UseCppExternalTypes.use_enum(input)
        return None(native_result)

    @staticmethod

    def use_class(input: ClassWithOverloads):
        """"""
        native_result = generated.UseCppExternalTypes.use_class(input)
        return None(native_result)

