

from smoke.TypesWithDefaultsImmutableStructWithCollections import TypesWithDefaultsImmutableStructWithCollections
from smoke.TypesWithDefaultsSomeImmutableStructWithDefaults import TypesWithDefaultsSomeImmutableStructWithDefaults


from _native_base import _NativeBase

import generated


class TypesWithDefaults(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], TypesWithDefaults):
            super().__init__(args[0])
        else:
            super().__init__(generated.TypesWithDefaults(*[getattr(arg, "_native", arg) for arg in args]))

