



from _native_base import _NativeBase

import generated


class CrossFileConstants(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], CrossFileConstants):
            super().__init__(args[0])
        else:
            super().__init__(generated.CrossFileConstants(*args))


FOO_BAR = StateEnum.ON

