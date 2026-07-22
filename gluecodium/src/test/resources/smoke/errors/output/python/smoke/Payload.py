

from __future__ import annotations



from _native_base import _NativeBase

import generated


class Payload(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], Payload):
            super().__init__(args[0])
        else:
            super().__init__(generated.Payload(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def error_code(self) -> int:
        """"""
        return self._native.error_code

    @error_code.setter
    def error_code(self, value: int):
      self._native.error_code = getattr(value, "_native", value)



    @property
    def message(self) -> str:
        """"""
        return self._native.message

    @message.setter
    def message(self, value: str):
      self._native.message = getattr(value, "_native", value)


