

from smoke.DartInternalClassWithInternalTypedef import DartInternalClassWithInternalTypedef
import typing

from _native_base import _NativeBase

import generated


class SomeDartClassThatUsesInternal(_NativeBase):
    """"""

    def __init__(self, native):
        super().__init__(native)

    def add_entity(self, entity: DartInternalClassWithInternalTypedef): ...

