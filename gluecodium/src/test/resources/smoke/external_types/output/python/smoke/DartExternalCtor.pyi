



from _native_base import _NativeBase

import generated


class DartExternalCtor(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], DartExternalCtor):
            super().__init__(args[0])
        else:
            super().__init__(generated.DartExternalCtor(*args))


    @property
    def field(self) -> str:
        """"""
        return self._native.field

    @field.setter
    def field(self, value: str):
        self._native.field = value


    @staticmethod

    def make(field: str) -> DartExternalCtor:
        """"""
        native_result = generated.DartExternalCtor.make(field)
        return DartExternalCtor(native_result)

