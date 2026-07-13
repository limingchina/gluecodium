



from _native_base import _NativeBase

import generated


class ParentInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, ParentInterface):
            super().__init__(native)
        else:
            super().__init__(generated.ParentInterface())


    def root_method(self):
        """"""
        return self._native.root_method()


    @property
    def root_property(self) -> str:
        """"""
        return self._native.root_property

    @root_property.setter
    def root_property(self, value: str):
        self._native.root_property = value

