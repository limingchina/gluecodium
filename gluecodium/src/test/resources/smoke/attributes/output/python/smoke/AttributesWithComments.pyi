

from smoke.PI import PI

from _native_base import _NativeBase


class AttributesWithComments(_NativeBase):
    """Class comment"""

    def __init__(self, native):
        super().__init__(native)

    Function comment
    def very_fun(self):
        """Function comment"""
        return self._native.very_fun()

    Property comment
    @property
    def prop(self) -> str:
        """Property comment"""
        return self._native.prop


