



from _native_base import _NativeBase

import generated


class NullableCollectionsStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], NullableCollectionsStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.NullableCollectionsStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def dates(self) -> list[Optional[datetime.datetime]]:
        """"""
        return self._native.dates

    @dates.setter
    def dates(self, value: list[Optional[datetime.datetime]]):
      self._native.dates = getattr(value, "_native", value)



    @property
    def structs(self) -> dict[int, Optional[NullableSomeStruct]]:
        """"""
        return self._native.structs

    @structs.setter
    def structs(self, value: dict[int, Optional[NullableSomeStruct]]):
      self._native.structs = getattr(value, "_native", value)


