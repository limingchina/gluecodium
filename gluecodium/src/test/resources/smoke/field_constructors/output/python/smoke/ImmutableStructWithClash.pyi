

import typing


from _native_base import _NativeBase

import generated


class ImmutableStructWithClash(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.ImmutableStructWithClash):
            super().__init__(args[0])
        else:
            super().__init__(generated.ImmutableStructWithClash(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def string_field(self) -> str:
        """"""
        return self._native.string_field



    @property
    def int_field(self) -> int:
        """"""
        return self._native.int_field



    @property
    def bool_field(self) -> bool:
        """"""
        return self._native.bool_field


