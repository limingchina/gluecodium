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

"""Field-constructor tests for the Python (pybind11) bindings."""

import functional
from test.FieldConstructorsPartialDefaults import FieldConstructorsPartialDefaults
from test.FieldConstructorsAllDefaults import FieldConstructorsAllDefaults
from test.MutableStructNoClash import MutableStructNoClash
from test.ImmutableStructNoClash import ImmutableStructNoClash
from test.ImmutableStructWithClash import ImmutableStructWithClash
from test.FieldConstructorsInternalFields import FieldConstructorsInternalFields
from test.FieldConstructorsExposeInternal import FieldConstructorsExposeInternal
from test.FieldConstructorsWithLabels import FieldConstructorsWithLabels
from test.FieldConstructorsParameterDefaults import FieldConstructorsParameterDefaults
from test.FieldCustomConstructorsMix import FieldCustomConstructorsMix
from test.OuterStructWithFieldConstructor import OuterStructWithFieldConstructor
from test.OuterStructWithFieldConstructorInnerStructWithDefaults import (
    OuterStructWithFieldConstructorInnerStructWithDefaults as InnerStructWithDefaults,
)
from test.ImmutableNamelessCtor import ImmutableNamelessCtor
from test.ImmutableDefaultCtor import ImmutableDefaultCtor
from test.MutableStructImmutableFields import MutableStructImmutableFields
from test.MutableStructImmutableFieldsNameless import MutableStructImmutableFieldsNameless
from test.MutableStructImmutableFieldsDefault import MutableStructImmutableFieldsDefault

import pytest


class TestFieldConstructorsPartialDefaults:
    def test_default_constructor(self):
        instance = FieldConstructorsPartialDefaults()
        assert instance.string_field == ""
        assert instance.int_field == 0
        assert instance.bool_field is True

    def test_partial_constructor(self):
        instance = FieldConstructorsPartialDefaults(7, "hello")
        assert instance.string_field == "hello"
        assert instance.int_field == 7
        assert instance.bool_field is True

    def test_full_constructor(self):
        instance = FieldConstructorsPartialDefaults(False, 11, "world")
        assert instance.string_field == "world"
        assert instance.int_field == 11
        assert instance.bool_field is False


class TestFieldConstructorsAllDefaults:
    def test_no_arg_constructor(self):
        instance = FieldConstructorsAllDefaults()
        assert instance.string_field == "nonsense"
        assert instance.int_field == 42
        assert instance.bool_field is True

    def test_single_arg_constructor(self):
        instance = FieldConstructorsAllDefaults(5)
        assert instance.int_field == 5

    def test_two_arg_constructor(self):
        instance = FieldConstructorsAllDefaults(5, "abc")
        assert instance.int_field == 5
        assert instance.string_field == "abc"

    def test_full_constructor(self):
        instance = FieldConstructorsAllDefaults(False, 9, "xyz")
        assert instance.bool_field is False
        assert instance.int_field == 9
        assert instance.string_field == "xyz"


class TestMutableStructNoClash:
    def test_no_arg_constructor(self):
        instance = MutableStructNoClash()
        assert instance.string_field == "nonsense"
        assert instance.int_field == 42
        assert instance.bool_field is True


class TestImmutableStructs:
    def test_immutable_no_clash(self):
        instance = ImmutableStructNoClash()
        assert instance.string_field == "nonsense"

    def test_immutable_with_clash(self):
        instance = ImmutableStructWithClash()
        assert instance.string_field == "nonsense"
        other = ImmutableStructWithClash(False, 3, "q")
        assert other.bool_field is False
        assert other.int_field == 3
        assert other.string_field == "q"


class TestInternalFields:
    def test_default_constructor(self):
        instance = FieldConstructorsInternalFields()
        assert instance.string_field == "nonsense"
        assert instance.int_field == 42

    def test_partial_constructor(self):
        instance = FieldConstructorsInternalFields(7, "hello")
        assert instance.int_field == 7
        assert instance.string_field == "hello"


class TestExposeInternal:
    def test_default_constructor(self):
        # @Internal fields are filtered out from the Python API, so the struct
        # is constructed with no visible arguments.
        instance = FieldConstructorsExposeInternal()
        assert instance is not None

    def test_internal_field_constructor(self):
        # The @Internal field constructor is filtered out from Python, so the
        # struct can only be default-constructed.
        instance = FieldConstructorsExposeInternal()
        assert instance is not None


class TestWithLabels:
    def test_default_constructor(self):
        instance = FieldConstructorsWithLabels()
        assert instance.string_field == "nonsense"

    def test_partial_constructor(self):
        instance = FieldConstructorsWithLabels(3, True)
        assert instance.int_field == 3
        assert instance.bool_field is True

    def test_full_constructor(self):
        instance = FieldConstructorsWithLabels("a", 4, False)
        assert instance.string_field == "a"
        assert instance.int_field == 4
        assert instance.bool_field is False


class TestParameterDefaults:
    def test_single_arg_constructor(self):
        instance = FieldConstructorsParameterDefaults(3)
        assert instance.int_field == 3

    def test_two_arg_constructor(self):
        instance = FieldConstructorsParameterDefaults(3, False)
        assert instance.int_field == 3
        assert instance.bool_field is False

    def test_full_constructor(self):
        instance = FieldConstructorsParameterDefaults("a", 4, True)
        assert instance.string_field == "a"
        assert instance.int_field == 4
        assert instance.bool_field is True


class TestCustomConstructorsMix:
    def test_default_constructor(self):
        instance = FieldCustomConstructorsMix()
        assert instance.string_field == "nonsense"

    def test_field_constructor(self):
        instance = FieldCustomConstructorsMix(9)
        assert instance.int_field == 9

    def test_create_me_static(self):
        instance = FieldCustomConstructorsMix.create_me(5, 1.0)
        assert instance.int_field == 5


class TestNesting:
    def test_field_constructor_with_inner_struct(self):
        inner = InnerStructWithDefaults()
        instance = OuterStructWithFieldConstructor(inner)
        assert instance.outer_struct_field.inner_struct_field == 1.0


class TestImmutableInit:
    def test_immutable_nameless_ctor(self):
        instance = ImmutableNamelessCtor()
        assert instance.string_field == ""

    def test_immutable_default_ctor(self):
        instance = ImmutableDefaultCtor()
        assert instance.string_field == ""

    def test_mutable_struct_immutable_fields(self):
        instance = MutableStructImmutableFields()
        assert instance.int_field == 42

    def test_mutable_struct_immutable_fields_nameless(self):
        instance = MutableStructImmutableFieldsNameless()
        assert instance.int_field == 42

    def test_mutable_struct_immutable_fields_default(self):
        instance = MutableStructImmutableFieldsDefault()
        assert instance.int_field == 42
