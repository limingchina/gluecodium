

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional


from enum import Enum

import generated


class RouteUtilsRouteType(Enum):
    """"""

    NONE = generated.smoke_RouteUtilsRouteType.NONE
    CAR = generated.smoke_RouteUtilsRouteType.CAR
    PEDESTRIAN = generated.smoke_RouteUtilsRouteType.PEDESTRIAN
    EQUESTRIAN = generated.smoke_RouteUtilsRouteType.EQUESTRIAN

    @property
    def _native(self):
        return self.value

