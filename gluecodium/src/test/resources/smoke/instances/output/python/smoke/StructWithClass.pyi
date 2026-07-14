

from smoke.SimpleClass import SimpleClass


from _native_base import _NativeBase

import generated


class StructWithClass(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithClass):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithClass(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def class_instance(self) -> SimpleClass:
        """"""
        return SimpleClass(self._native.class_instance)

    @class_instance.setter
    def class_instance(self, value: SimpleClass):
      self._native.class_instance = getattr(value, "_native", value)


