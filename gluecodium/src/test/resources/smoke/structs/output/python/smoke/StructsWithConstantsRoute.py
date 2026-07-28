

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.RouteUtilsRouteType import RouteUtilsRouteType


from _native_base import _NativeBase

import generated


class StructsWithConstantsRoute(_NativeBase):
    """"""

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and not kwargs and isinstance(args[0], generated.smoke_StructsWithConstantsRoute):
            super().__init__(args[0])
        else:
            super().__init__(generated.smoke_StructsWithConstantsRoute(
                *[_unwrap(arg) for arg in args],
                **{k: _unwrap(v) for k, v in kwargs.items()}
            ))


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


    DEFAULT_TYPE = RouteUtilsRouteType.EQUESTRIAN

