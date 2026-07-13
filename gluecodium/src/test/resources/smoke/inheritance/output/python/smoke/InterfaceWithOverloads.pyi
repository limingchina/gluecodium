



from _native_base import _NativeBase

import generated


class InterfaceWithOverloads(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, InterfaceWithOverloads):
            super().__init__(native)
        else:
            super().__init__(generated.InterfaceWithOverloads())


    def parent_method(self):
        """"""
        return self._native.parent_method()


    def parent_method(self, input: str):
        """"""
        return self._native.parent_method(input)

