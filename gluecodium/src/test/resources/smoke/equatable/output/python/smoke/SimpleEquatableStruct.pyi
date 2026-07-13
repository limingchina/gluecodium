

from smoke.NonEquatableClass import NonEquatableClass
from smoke.NonEquatableInterface import NonEquatableInterface

from _native_base import _NativeBase


class SimpleEquatableStruct(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)


    class_field: NonEquatableClass


    interface_field: NonEquatableInterface


    nullable_class_field: Optional[NonEquatableClass]


    nullable_interface_field: Optional[NonEquatableInterface]

