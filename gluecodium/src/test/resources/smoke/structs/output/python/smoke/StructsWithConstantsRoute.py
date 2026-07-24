

from __future__ import annotations

from _native_base import _unwrap, _wrap
from typing import Optional

from smoke.RouteUtilsRouteType import RouteUtilsRouteType


from _native_base import _NativeBase

import generated


class StructsWithConstantsRoute(_NativeBase):
    """"""

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], generated.StructsWithConstantsRoute):
            super().__init__(args[0])
        else:
            super().__init__(generated.StructsWithConstantsRoute(*[_unwrap(arg) for arg in args]))


    @property
    def description(self) -> str:
        """"""
        return _wrap(self._native.description, str)
    @description.setter
    def description(self, value: str):
      self._native.description = _unwrap(value, str)



    @property
    def type(self) -> RouteUtilsRouteType:
        """"""
        return _wrap(self._native.type, RouteUtilsRouteType)
    @type.setter
    def type(self, value: RouteUtilsRouteType):
      self._native.type = _unwrap(value, RouteUtilsRouteType)



    DEFAULT_DESCRIPTION = "Nonsense"


    DEFAULT_TYPE = RouteType.EQUESTRIAN

