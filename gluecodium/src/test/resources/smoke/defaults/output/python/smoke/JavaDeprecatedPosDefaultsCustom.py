

from __future__ import annotations



from _native_base import _NativeBase

import generated


class JavaDeprecatedPosDefaultsCustom(_NativeBase):
    """Foo Bar this is a comment"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.JavaDeprecatedPosDefaultsCustom):
            super().__init__(args[0])
        else:
            super().__init__(generated.JavaDeprecatedPosDefaultsCustom(*[getattr(arg, "_native", arg) for arg in args]))

    first init!
    @property
    def first_init_field(self) -> int:
        """first init!"""
        return self._native.first_init_field
    @first_init_field.setter
    def first_init_field(self, value: int):
      self._native.first_init_field = getattr(value, "_native", value)


    first free!
    @property
    def first_free_field(self) -> str:
        """first free!"""
        return self._native.first_free_field
    @first_free_field.setter
    def first_free_field(self, value: str):
      self._native.first_free_field = getattr(value, "_native", value)


    @staticmethod
    def custom() -> JavaDeprecatedPosDefaultsCustom:
        """"""
        native_result = generated.JavaDeprecatedPosDefaultsCustom.custom()
        return JavaDeprecatedPosDefaultsCustom(native_result)

