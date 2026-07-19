

from smoke.SimpleInterface import SimpleInterface


from _native_base import _NativeBase

import generated


class StructWithInterface(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructWithInterface):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithInterface(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def interface_instance(self) -> SimpleInterface:
        """"""
        return SimpleInterface(self._native.interface_instance)
    @interface_instance.setter
    def interface_instance(self, value: SimpleInterface):
      self._native.interface_instance = getattr(value, "_native", value)


