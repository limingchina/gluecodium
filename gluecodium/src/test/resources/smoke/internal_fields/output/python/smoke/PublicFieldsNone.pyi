



from _native_base import _NativeBase

import generated


class PublicFieldsNone(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PublicFieldsNone):
            super().__init__(args[0])
        else:
            super().__init__(generated.PublicFieldsNone(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def internal_field(self) -> str:
        """"""
        return self._native.internal_field
    @internal_field.setter
    def internal_field(self, value: str):
      self._native.internal_field = getattr(value, "_native", value)


