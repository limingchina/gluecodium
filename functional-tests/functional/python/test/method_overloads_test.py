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
from test.MethodOverloadsPoint import MethodOverloadsPoint
from test.ConstructorOverloads import ConstructorOverloads
from test.StructConstructorOverloads import StructConstructorOverloads

import pytest


class TestMethodOverloads:
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
