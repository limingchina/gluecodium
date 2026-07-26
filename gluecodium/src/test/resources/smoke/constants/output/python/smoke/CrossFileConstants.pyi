

from smoke.ConstantsStateEnum import ConstantsStateEnum
import typing


from _native_base import _NativeBase

import generated


class CrossFileConstants(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.smoke_CrossFileConstants):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_CrossFileConstants(*[_unwrap(arg) for arg in args]))


    FOO_BAR = ConstantsStateEnum.ON

