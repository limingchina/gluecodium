



from _native_base import _NativeBase

import generated


class AttributesWithComments(_NativeBase):
    """Class comment"""

    def __init__(self, native):
        super().__init__(native)

    def very_fun(self):
        """Function comment"""
        return self._native.very_fun()

    Property comment
    @property
    def prop(self) -> str:
        """Property comment"""
        return self._native.prop

    @prop.setter
    def prop(self, value: str):
        self._native.prop = value

Const comment
PI = False

