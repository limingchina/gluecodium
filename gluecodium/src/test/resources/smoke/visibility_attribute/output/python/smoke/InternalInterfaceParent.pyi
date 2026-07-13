



from _native_base import _NativeBase

import generated


class InternalInterfaceParent(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, InternalInterfaceParent):
            super().__init__(native)
        else:
            super().__init__(generated.InternalInterfaceParent())


    def foo_bar(self):
        """"""
        return self._native.foo_bar()


    @property
    def prop(self) -> str:
        """"""
        return self._native.prop

    @prop.setter
    def prop(self, value: str):
        self._native.prop = value

