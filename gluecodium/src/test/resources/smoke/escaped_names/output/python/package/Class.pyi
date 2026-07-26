

from package.Interface import Interface
from package.typesenum import typesenum
from package.typesexception import typesexception
from package.typesstruct import typesstruct
import typing

import generated


class Class(generated.package_Class):
    """"""

    def __init__(self, native=None):
        # Subclass the native pybind11 type so a Python override of an inherited virtual
        # method (from a parent interface or open base class) is dispatched through the
        # generated trampoline. When `native` is an existing native instance (returned by
        # a factory), adopt it via the generated adoption constructor; otherwise construct a
        # fresh trampoline. `self._native` aliases the wrapper itself so the rest of the
        # generated code can reach the native object uniformly.
        if native is not None and isinstance(native, generated.package_Class):
            super().__init__(native)
        else:
            super().__init__()
        self._native = self

    @staticmethod
    def constructor() -> Class: ...

    def fun(self, double: list[typesstruct]) -> typesstruct: ...

    @property
    def property(self) -> typesenum:
        """"""
        return _wrap(generated.package_Class.property.fget(self), typesenum)

    @property.setter
    def property(self, value: typesenum):
        generated.package_Class.property.fset(self, _unwrap(value, typesenum))

