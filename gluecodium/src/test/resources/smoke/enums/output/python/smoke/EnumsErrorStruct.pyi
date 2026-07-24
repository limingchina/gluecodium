

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
            super().__init__(generated.EnumsErrorStruct(*[_unwrap(arg) for arg in args]))


    @property
    def type(self) -> EnumsInternalErrorCode:
        """"""
        return _wrap(self._native.type, EnumsInternalErrorCode)
    @type.setter
    def type(self, value: EnumsInternalErrorCode):
      self._native.type = _unwrap(value, EnumsInternalErrorCode)



    @property
    def message(self) -> str:
        """"""
        return _wrap(self._native.message, str)
    @message.setter
    def message(self, value: str):
      self._native.message = _unwrap(value, str)


