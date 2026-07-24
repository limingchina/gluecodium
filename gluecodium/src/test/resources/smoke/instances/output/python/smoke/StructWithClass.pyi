

from smoke.SimpleClass import SimpleClass
import typing


from _native_base import _NativeBase

import generated


class StructWithClass(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructWithClass):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithClass(*[_unwrap(arg) for arg in args]))


    @property
    def class_instance(self) -> SimpleClass:
        """"""
        return _wrap(self._native.class_instance, SimpleClass)
    @class_instance.setter
    def class_instance(self, value: SimpleClass):
      self._native.class_instance = _unwrap(value, SimpleClass)


