



from _native_base import _NativeBase

import generated


class Currency(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Currency):
            super().__init__(args[0])
        else:
            super().__init__(generated.Currency(*args))


    @property
    def currency_code(self) -> str:
        """"""
        return self._native.currency_code

    @currency_code.setter
    def currency_code(self, value: str):
        self._native.currency_code = value



    @property
    def numeric_code(self) -> int:
        """"""
        return self._native.numeric_code

    @numeric_code.setter
    def numeric_code(self, value: int):
        self._native.numeric_code = value


