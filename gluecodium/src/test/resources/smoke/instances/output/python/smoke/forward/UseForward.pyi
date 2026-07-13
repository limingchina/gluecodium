

from smoke.SimpleClass import SimpleClass
from smoke.SimpleInterface import SimpleInterface
from smoke.forward.Class1 import Class1
from smoke.forward.Class2 import Class2


from _native_base import _NativeBase

import generated


class UseForward(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, UseForward):
            super().__init__(native)
        else:
            super().__init__(generated.UseForward())


    def use_it(self, param1: Class1, param2: Class2, simple_class: SimpleClass, simple_interface: SimpleInterface):
        """"""
        return self._native.use_it(param1._native, param2._native, simple_class._native, simple_interface._native)

