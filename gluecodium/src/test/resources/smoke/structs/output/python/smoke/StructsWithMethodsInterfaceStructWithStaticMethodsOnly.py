

from __future__ import annotations



from _native_base import _NativeBase

import generated


class StructsWithMethodsInterfaceStructWithStaticMethodsOnly(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsWithMethodsInterfaceStructWithStaticMethodsOnly):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithMethodsInterfaceStructWithStaticMethodsOnly(*[getattr(arg, "_native", arg) for arg in args]))

    @staticmethod
    def do_stuff():
        """"""
        generated.StructsWithMethodsInterfaceStructWithStaticMethodsOnly.do_stuff()

