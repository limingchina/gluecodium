



from _native_base import _NativeBase

import generated


class InterfaceWithLambda(_NativeBase):
    """"""

    def __init__(self, native=None):
        if isinstance(native, InterfaceWithLambda):
            super().__init__(native)
        else:
            super().__init__(generated.InterfaceWithLambda())

