



from _native_base import _NativeBase

import generated


class FieldConstructorWithExcluded(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and hasattr(args[0], "_native"):
            super().__init__(args[0]._native)
        else:
            super().__init__(generated.FieldConstructorWithExcluded(*[getattr(arg, "_native", arg) for arg in args]))

    Some field
    @property
    def string_field(self) -> str:
        """Some field"""
        return self._native.string_field
    @string_field.setter
    def string_field(self, value: str):
      self._native.string_field = getattr(value, "_native", value)


