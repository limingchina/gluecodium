

from smoke.NonEquatableClass import NonEquatableClass
from smoke.NonEquatableInterface import NonEquatableInterface

class SimpleEquatableStruct:
    """"""

    def __init__(self, native):
        self._native = native


    class_field: NonEquatableClass


    interface_field: NonEquatableInterface


    nullable_class_field: Optional[NonEquatableClass]


    nullable_interface_field: Optional[NonEquatableInterface]

