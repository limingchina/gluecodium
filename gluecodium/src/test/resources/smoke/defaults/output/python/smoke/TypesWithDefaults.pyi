

from smoke.ImmutableStructWithCollections import ImmutableStructWithCollections
from smoke.SomeImmutableStructWithDefaults import SomeImmutableStructWithDefaults


from _native_base import _NativeBase

import generated


class TypesWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], TypesWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypesWithDefaults(*args))

