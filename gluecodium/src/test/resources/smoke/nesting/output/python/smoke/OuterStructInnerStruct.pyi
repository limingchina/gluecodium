

import typing


from _native_base import _NativeBase

import generated


class OuterStructInnerStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.OuterStructInnerStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.OuterStructInnerStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def other_field(self) -> list[datetime.datetime]:
        """"""
        return self._native.other_field
    @other_field.setter
    def other_field(self, value: list[datetime.datetime]):
      self._native.other_field = getattr(value, "_native", value)


    def do_something(self): ...

