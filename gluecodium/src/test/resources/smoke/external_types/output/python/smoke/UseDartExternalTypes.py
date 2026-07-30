

from __future__ import annotations

from _native_base import _unwrap, _wrap, _get_or_create_wrapper
from typing import Optional

from smoke.CompressionState import CompressionState
from smoke.DartColor import DartColor
from smoke.DartSeason import DartSeason
from smoke.Rectangle import Rectangle

from _native_base import _NativeBase

import generated


class UseDartExternalTypes(_NativeBase):
    def __init__(self, native):
        super().__init__(native)

    @staticmethod
    def rectangle_round_trip(input: Rectangle) -> Rectangle:
        native_result = generated.smoke_UseDartExternalTypes.rectangle_round_trip(_unwrap(input, Rectangle))
        return _get_or_create_wrapper(native_result, Rectangle)

    @staticmethod
    def compression_state_round_trip(input: CompressionState) -> CompressionState:
        native_result = generated.smoke_UseDartExternalTypes.compression_state_round_trip(_unwrap(input, CompressionState))
        return _get_or_create_wrapper(native_result, CompressionState)

    @staticmethod
    def color_round_trip(input: DartColor) -> DartColor:
        native_result = generated.smoke_UseDartExternalTypes.color_round_trip(_unwrap(input, DartColor))
        return _get_or_create_wrapper(native_result, DartColor)

    @staticmethod
    def season_round_trip(input: DartSeason) -> DartSeason:
        native_result = generated.smoke_UseDartExternalTypes.season_round_trip(_unwrap(input, DartSeason))
        return _get_or_create_wrapper(native_result, DartSeason)

