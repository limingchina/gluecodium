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

"""Struct immutability tests for the Python (pybind11) bindings."""

from test.PlainDataStructuresImmutable import PlainDataStructuresImmutable

AllTypesImmutableStruct = PlainDataStructuresImmutable.AllTypesImmutableStruct
NestingImmutableStruct = PlainDataStructuresImmutable.NestingImmutableStruct
Point = PlainDataStructuresImmutable.Point
StructWithArrayOfImmutable = PlainDataStructuresImmutable.StructWithArrayOfImmutable

import pytest


class TestStructsImmutable:
    def test_create_all_types_immutable_struct(self):
        point = Point(1.0, 2.0)
        struct = AllTypesImmutableStruct(
            int8_field=0,
            uint8_field=0,
            int16_field=0,
            uint16_field=0,
            int32_field=0,
            uint32_field=0,
            int64_field=0,
            uint64_field=0,
            float_field=0.0,
            double_field=0.0,
            string_field="",
            boolean_field=False,
            point_field=point,
        )

        assert struct.int8_field == 0
        assert struct.string_field == ""
        assert struct.point_field.x == 1.0

    def test_nesting_immutable_struct(self):
        point = Point(1.0, 2.0)
        all_types = AllTypesImmutableStruct(
            int8_field=1,
            uint8_field=2,
            int16_field=3,
            uint16_field=4,
            int32_field=5,
            uint32_field=6,
            int64_field=7,
            uint64_field=8,
            float_field=9.0,
            double_field=10.0,
            string_field="test",
            boolean_field=True,
            point_field=point,
        )
        nesting = NestingImmutableStruct(struct_field=all_types)

        assert nesting.struct_field.int8_field == 1
        assert nesting.struct_field.point_field.x == 1.0

    def test_immutable_struct_field_is_readonly(self):
        point = Point(1.0, 2.0)
        struct = AllTypesImmutableStruct(
            int8_field=0,
            uint8_field=0,
            int16_field=0,
            uint16_field=0,
            int32_field=0,
            uint32_field=0,
            int64_field=0,
            uint64_field=0,
            float_field=0.0,
            double_field=0.0,
            string_field="",
            boolean_field=False,
            point_field=point,
        )

        with pytest.raises(AttributeError):
            struct.string_field = "new value"

    def test_immutable_struct_round_trip(self):
        point = Point(1.0, 2.0)
        struct = AllTypesImmutableStruct(
            int8_field=42,
            uint8_field=255,
            int16_field=1000,
            uint16_field=2000,
            int32_field=3000,
            uint32_field=4000,
            int64_field=5000,
            uint64_field=6000,
            float_field=3.14,
            double_field=2.718,
            string_field="hello",
            boolean_field=True,
            point_field=point,
        )

        result = PlainDataStructuresImmutable.immutable_struct_round_trip(struct)

        assert result.int8_field == 42
        assert result.string_field == "hello"
        assert result.point_field.x == 1.0