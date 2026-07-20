

import typing


from _native_base import _NativeBase

import generated


class PublicClassPublicStructWithInternalDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.PublicClassPublicStructWithInternalDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.PublicClassPublicStructWithInternalDefaults(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def internal_field(self) -> str:
        """"""
        return self._native.internal_field
    @internal_field.setter
    def internal_field(self, value: str):
      self._native.internal_field = getattr(value, "_native", value)



    @property
    def public_field(self) -> float:
        """"""
        return self._native.public_field
    @public_field.setter
    def public_field(self, value: float):
      self._native.public_field = getattr(value, "_native", value)


