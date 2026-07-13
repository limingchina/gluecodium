

from smoke.ParentInterface import ParentInterface


from _native_base import _NativeBase

import generated


class CrossPackageChildInterface(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, CrossPackageChildInterface):
            super().__init__(native)
        else:
            super().__init__(generated.CrossPackageChildInterface())

