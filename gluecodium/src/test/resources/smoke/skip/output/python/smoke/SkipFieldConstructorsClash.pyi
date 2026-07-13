



from _native_base import _NativeBase

import generated


class SkipFieldConstructorsClash(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], SkipFieldConstructorsClash):
            super().__init__(args[0])
        else:
            super().__init__(generated.SkipFieldConstructorsClash(*args))


    @property
    def param(self) -> str:
        """"""
        return self._native.param

    @param.setter
    def param(self, value: str):
        self._native.param = value


