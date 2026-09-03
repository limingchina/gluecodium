

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper, _NativeBase
from enum import Enum
from typing import Optional
import generated

from smoke.DateInterval import DateInterval
from smoke.Persistence import Persistence
from smoke.PseudoColor import PseudoColor
from smoke.SwiftSeason import SwiftSeason

class UseSwiftExternalTypes(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def date_interval_round_trip(input: DateInterval) -> DateInterval:
        native_result = generated.smoke_UseSwiftExternalTypes.date_interval_round_trip(_unwrap(input, DateInterval))
        return _get_or_create_wrapper(native_result, DateInterval)

    @staticmethod
    def persistence_round_trip(input: Persistence) -> Persistence:
        native_result = generated.smoke_UseSwiftExternalTypes.persistence_round_trip(_unwrap(input, Persistence))
        return _get_or_create_wrapper(native_result, Persistence)

    @staticmethod
    def color_round_trip(input: PseudoColor) -> PseudoColor:
        native_result = generated.smoke_UseSwiftExternalTypes.color_round_trip(_unwrap(input, PseudoColor))
        return _get_or_create_wrapper(native_result, PseudoColor)

    @staticmethod
    def season_round_trip(input: SwiftSeason) -> SwiftSeason:
        native_result = generated.smoke_UseSwiftExternalTypes.season_round_trip(_unwrap(input, SwiftSeason))
        return _get_or_create_wrapper(native_result, SwiftSeason)


