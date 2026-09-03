# Copyright (C) 2016-2025 HERE Europe B.V.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# License-Filename: LICENSE

"""Struct-in-type-collection mapping tests for the Python (pybind11) bindings."""

import functional
from test.TypeCollection import TypeCollection
from test.PlainDataStructuresFromTypeCollection import (
    PlainDataStructuresFromTypeCollection,
)

Color = TypeCollection.Color
ColoredLine = TypeCollection.ColoredLine
Line = TypeCollection.Line
Point = TypeCollection.Point
AllTypesStruct = TypeCollection.AllTypesStruct

import pytest


class TestStructsInTypes:
    def test_create_point(self):
        point = PlainDataStructuresFromTypeCollection.create_point(1.0, 2.0)

        assert isinstance(point, Point)
        assert point.x == 1.0
        assert point.y == 2.0

    def test_swap_point_coordinates(self):
        point = PlainDataStructuresFromTypeCollection.create_point(1.0, 2.0)
        swapped = PlainDataStructuresFromTypeCollection.swap_point_coordinates(point)

        assert swapped.x == 2.0
        assert swapped.y == 1.0

    def test_nested_struct(self):
        line = PlainDataStructuresFromTypeCollection.create_line(
            Point(1.0, 2.0), Point(3.0, 4.0)
        )

        assert isinstance(line, Line)
        assert line.a.x == 1.0
        assert line.b.y == 4.0

    def test_colored_line(self):
        line = PlainDataStructuresFromTypeCollection.create_line(
            Point(0.0, 0.0), Point(1.0, 1.0)
        )
        color = Color()
        color.red = 10
        color.green = 20
        color.blue = 30
        colored = PlainDataStructuresFromTypeCollection.create_colored_line(line, color)

        assert isinstance(colored, ColoredLine)
        assert colored.color.red == 10
        assert colored.line.b.x == 1.0

    def test_modify_all_types_struct(self):
        point = Point(1.0, 2.0)
        struct = AllTypesStruct(
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9.0,
            10.0,
            "test",
            False,
            point,
        )

        result = PlainDataStructuresFromTypeCollection.modify_all_types_struct(struct)

        assert result.int8_field == 2
        assert result.uint8_field == 3
        assert result.string_field == "Hello test"
        assert result.boolean_field is True
        assert result.point_field.x == 2.0
        assert result.point_field.y == 1.0
