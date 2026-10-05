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

"""Method overload mapping tests for the Python (pybind11) bindings."""

import functional
from test.MethodOverloads import MethodOverloads
from test.ConstructorOverloads import ConstructorOverloads
from test.StructConstructorOverloads import StructConstructorOverloads

MethodOverloadsPoint = MethodOverloads.Point

import pytest


class TestMethodOverloads:
    @pytest.mark.parametrize(
        "value, expected",
        [(True, True), (5, False), ("text", False), ([1, 2, 3], False), ({"a", "b"}, False)],
    )
    def test_is_boolean_keyword(self, value, expected):
        assert MethodOverloads.is_boolean(input=value) is expected

    def test_is_boolean_wrapper_keyword(self):
        assert MethodOverloads.is_boolean(input=MethodOverloadsPoint(1.0, 2.0)) is False

    def test_is_boolean_mixed_arguments(self):
        assert MethodOverloads.is_boolean(
            True, 5, input3="text", input4=MethodOverloadsPoint(1.0, 2.0)
        ) is False

    def test_is_boolean_rejects_duplicate_argument(self):
        with pytest.raises(TypeError):
            MethodOverloads.is_boolean(True, input=True)

    def test_is_boolean_rejects_unknown_keyword(self):
        with pytest.raises(TypeError):
            MethodOverloads.is_boolean(True, unknown=True)

    def test_is_boolean_bool(self):
        assert MethodOverloads.is_boolean(True) is True

    def test_is_boolean_byte(self):
        assert MethodOverloads.is_boolean(5) is False

    def test_is_boolean_string(self):
        assert MethodOverloads.is_boolean("text") is False

    def test_is_boolean_point(self):
        assert MethodOverloads.is_boolean(MethodOverloadsPoint(1.0, 2.0)) is False

    def test_is_boolean_multi(self):
        assert MethodOverloads.is_boolean(True, 5, "text", MethodOverloadsPoint(1.0, 2.0)) is False

    def test_is_boolean_string_list(self):
        assert MethodOverloads.is_boolean(["a", "b"]) is False

    def test_is_boolean_byte_list(self):
        assert MethodOverloads.is_boolean([1, 2, 3]) is False

    def test_is_boolean_string_set(self):
        assert MethodOverloads.is_boolean({"a", "b"}) is False

    def test_is_boolean_byte_set(self):
        assert MethodOverloads.is_boolean({1, 2, 3}) is False


class TestConstructorOverloads:
    def test_create_mixed_arguments(self):
        instance = ConstructorOverloads.create("text", boolean_input=True)
        assert isinstance(instance, ConstructorOverloads)

    def test_create_rejects_invalid_keyword_value(self):
        # Dropping the keyword would incorrectly select the default constructor.
        with pytest.raises(TypeError):
            ConstructorOverloads.create(input=object())

    def test_create_rejects_unknown_keyword(self):
        with pytest.raises(TypeError):
            ConstructorOverloads.create(unknown="text")

    def test_create_no_args(self):
        instance = ConstructorOverloads.create()
        assert isinstance(instance, ConstructorOverloads)

    def test_create_string(self):
        instance = ConstructorOverloads.create("text")
        assert isinstance(instance, ConstructorOverloads)

    def test_create_bool(self):
        instance = ConstructorOverloads.create(True)
        assert isinstance(instance, ConstructorOverloads)

    def test_create_multi(self):
        instance = ConstructorOverloads.create("text", True)
        assert isinstance(instance, ConstructorOverloads)

    def test_create_list(self):
        instance = ConstructorOverloads.create([1.0, 2.0])
        assert isinstance(instance, ConstructorOverloads)

    def test_create_ulong(self):
        instance = ConstructorOverloads.create(42)
        assert isinstance(instance, ConstructorOverloads)


class TestStructConstructorOverloads:
    def test_create_keyword_selects_string_overload(self):
        instance = StructConstructorOverloads.create(input="text")
        assert isinstance(instance, StructConstructorOverloads)
        assert instance.string_field == "text"

    def test_create_keywords_select_two_string_overload(self):
        instance = StructConstructorOverloads.create(input2="bar", input1="foo")
        assert instance.string_field == "foobar"

    def test_create_mixed_arguments(self):
        instance = StructConstructorOverloads.create("foo", input2="bar")
        assert instance.string_field == "foobar"

    def test_create_no_args(self):
        instance = StructConstructorOverloads.create()
        assert isinstance(instance, StructConstructorOverloads)

    def test_create_string(self):
        instance = StructConstructorOverloads.create("text")
        assert isinstance(instance, StructConstructorOverloads)
        assert instance.string_field == "text"

    def test_create_two_strings(self):
        instance = StructConstructorOverloads.create("foo", "bar")
        assert isinstance(instance, StructConstructorOverloads)
        assert instance.string_field == "foobar"
