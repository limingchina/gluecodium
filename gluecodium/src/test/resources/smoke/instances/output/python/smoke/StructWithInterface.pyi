

from smoke.SimpleInterface import SimpleInterface


from _native_base import _NativeBase

import generated


class StructWithInterface(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], StructWithInterface):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructWithInterface(*args))


    @property
    def interface_instance(self) -> SimpleInterface:
        """"""
        return self._native.interface_instance

    @interface_instance.setter
    def interface_instance(self, value: SimpleInterface):
        self._native.interface_instance = value


