

from smoke.EnumsInternalErrorCode import EnumsInternalErrorCode
import typing


from _native_base import _NativeBase

import generated


class EnumsErrorStruct(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.EnumsErrorStruct):
            super().__init__(args[0])
        else:
            super().__init__(generated.EnumsErrorStruct(*[getattr(arg, "_native", arg) for arg in args]))


    @property
    def type(self) -> EnumsInternalErrorCode:
        """"""
        return EnumsInternalErrorCode(self._native.type)
    @type.setter
    def type(self, value: EnumsInternalErrorCode):
      self._native.type = getattr(value, "_native", value)



    @property
    def message(self) -> str:
        """"""
        return self._native.message
    @message.setter
    def message(self, value: str):
      self._native.message = getattr(value, "_native", value)


