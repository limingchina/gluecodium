

from smoke.PropertiesInterfaceExampleStruct import PropertiesInterfaceExampleStruct
import typing


import generated


class PropertiesInterface(generated.smoke_PropertiesInterface):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so that a Python override of an interface
        # method is dispatched through the generated trampoline. When `native` is an
        # existing native instance (returned by a factory), adopt it via the generated
        # adoption constructor; otherwise construct a fresh trampoline. `self._native`
        # aliases the wrapper itself so the rest of the generated code can reach the
        # native object uniformly (e.g. when passing this interface back into a C++
        # call site).
        if native is not None and isinstance(native, generated.smoke_PropertiesInterface):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @property
    def struct_property(self) -> PropertiesInterfaceExampleStruct:
        """"""
        return _wrap(generated.smoke_PropertiesInterface.struct_property.fget(self), PropertiesInterfaceExampleStruct)

    @struct_property.setter
    def struct_property(self, value: PropertiesInterfaceExampleStruct):
        generated.smoke_PropertiesInterface.struct_property.fset(self, _unwrap(value, PropertiesInterfaceExampleStruct))

