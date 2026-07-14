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

import functional
from test.PlainDataStructuresImmutableAllTypesImmutableStruct import (
    PlainDataStructuresImmutableAllTypesImmutableStruct as AllTypesImmutableStruct,
)
from test.PlainDataStructuresImmutableNestingImmutableStruct import (
    PlainDataStructuresImmutableNestingImmutableStruct as NestingImmutableStruct,
)
from test.PlainDataStructuresImmutablePoint import PlainDataStructuresImmutablePoint as Point
from test.PlainDataStructuresImmutableStructWithArrayOfImmutable import (
    PlainDataStructuresImmutableStructWithArrayOfImmutable as StructWithArrayOfImmutable,
)

import pytest


class TestStructsImmutable:
    def test_create_all_types_immutable_struct(self):
        point = Point(1.0, 2.0)
        struct = AllTypesImmutableStruct(
            int8Field=0,
            uint8Field=0,
            int16Field=0,
            uint16Field=0,
            int32Field=0,
            uint32Field=0,
            int64Field=0,
            uint64Field=0,
            floatField=0.0,
            doubleField=0.0,
            stringField="",
            booleanField=False,
            pointField=point,
        )

        assert struct.int8_field == 0
        assert struct.string_field == ""
        assert struct.point_field.x == 1.0

    def test_nesting_immutable_struct(self):
        point = Point(1.0, 2.0)
        all_types = AllTypesImmutableStruct(
            int8Field=1,
            uint8Field=2,
            int16Field=3,
            uint16Field=4,
            int32Field=5,
            uint32Field=6,
            int64Field=7,
            uint64Field=8,
            floatField=9.0,
            doubleField=10.0,
            stringField="test",
            booleanField=True,
            pointField=point,
        )
        nesting = NestingImmutableStruct(structField=all_types)

        assert nesting.struct_field.int8_field == 1
        assert nesting.struct_field.point_field.x == 1.0

    def test_immutable_struct_field_is_readonly(self):
        point = Point(1.0, 2.0)
        struct = AllTypesImmutableStruct(
            int8Field=0,
            uint8Field=0,
            int16Field=0,
            uint16Field=0,
            int32Field=0,
            uint32Field=0,
            int64Field=0,
            uint64Field=0,
            floatField=0.0,
            doubleField=0.0,
            stringField="",
            booleanField=False,
            pointField=point,
        )

        with pytest.raises(AttributeError):
            struct.string_field = "new value"

    def test_immutable_struct_round_trip(self):
        point = Point(1.0, 2.0)
        struct = AllTypesImmutableStruct(
            int8Field=42,
            uint8Field=255,
            int16Field=1000,
            uint16Field=2000,
            int32Field=3000,
            uint32Field=4000,
            int64Field=5000,
            uint64Field=6000,
            floatField=3.14,
            doubleField=2.718,
            stringField="hello",
            booleanField=True,
            pointField=point,
        )

        result = functional.PlainDataStructuresImmutable.immutableStructRoundTrip(struct)

        assert result.int8_field == 42
        assert result.string_field == "hello"
        assert result.point_field.x == 1.0