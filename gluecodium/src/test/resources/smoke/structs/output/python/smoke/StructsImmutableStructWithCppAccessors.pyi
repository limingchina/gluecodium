

from smoke.StructsPoint import StructsPoint
import typing


from _native_base import _NativeBase

import generated


class StructsImmutableStructWithCppAccessors(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsImmutableStructWithCppAccessors):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsImmutableStructWithCppAccessors(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def trivial_int_field(self) -> int:
        """"""
        return self._native.trivial_int_field



    @property
    def trivial_double_field(self) -> float:
        """"""
        return self._native.trivial_double_field



    @property
    def nontrivial_string_field(self) -> str:
        """"""
        return self._native.nontrivial_string_field



    @property
    def nontrivial_point_field(self) -> StructsPoint:
        """"""
        return StructsPoint(self._native.nontrivial_point_field)



    @property
    def nontrivial_optional_point(self):
        """"""
        return Optional[StructsPoint](self._native.nontrivial_optional_point)


