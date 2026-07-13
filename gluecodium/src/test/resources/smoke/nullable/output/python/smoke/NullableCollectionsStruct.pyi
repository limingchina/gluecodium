



from _native_base import _NativeBase

import generated


class NullableCollectionsStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], NullableCollectionsStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.NullableCollectionsStruct(*args))


    @property
    def dates(self) -> list[Optional[datetime.datetime]]:
        """"""
        return self._native.dates

    @dates.setter
    def dates(self, value: list[Optional[datetime.datetime]]):
        self._native.dates = value



    @property
    def structs(self) -> dict[int, Optional[SomeStruct]]:
        """"""
        return self._native.structs

    @structs.setter
    def structs(self, value: dict[int, Optional[SomeStruct]]):
        self._native.structs = value


