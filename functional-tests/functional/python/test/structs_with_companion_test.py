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

"""Struct-with-companion (methods + constants) tests for the Python (pybind11) bindings."""

import functional
from test.Vector import Vector
from test.RouteUtils import RouteUtils
from test.StructWithConstMethod import StructWithConstMethod
from test.StructsWithMethodsInterface import StructsWithMethodsInterface
from test.SimpleRoute import SimpleRoute
from test.StructsWithConstantsInterface import StructsWithConstantsInterface

Vector3 = StructsWithMethodsInterface.Vector3
InterfaceStaticMethodsOnly = StructsWithMethodsInterface.StructWithStaticMethodsOnly
MultiRoute = StructsWithConstantsInterface.MultiRoute
RouteType = RouteUtils.RouteType

import pytest


class TestStructsWithMethods:
    def test_vector_distance_to_self(self):
        vector = Vector(1.0, 2.0)

        assert isinstance(vector, Vector)
        assert vector.distance_to(vector) == 0.0

    def test_vector_distance_to_other(self):
        vector = Vector(1.0, 2.0)
        other = Vector(-3.0, -4.0)

        # sqrt((1 - -3)^2 + (2 - -4)^2) = sqrt(16 + 36) = sqrt(52) ≈ 7.211
        assert vector.distance_to(other) == pytest.approx(7.211, abs=0.001)

    def test_vector_add_self(self):
        vector = Vector(1.0, 2.0)
        result = vector.add(vector)

        assert result.x == 2.0
        assert result.y == 4.0

    def test_vector_add_other(self):
        vector = Vector(1.0, 2.0)
        other = Vector(-3.0, -7.0)
        result = vector.add(other)

        assert result.x == -2.0
        assert result.y == -5.0

    def test_vector_validate_passes(self):
        assert Vector.validate(1.0, 2.0) is True

    def test_vector_validate_fails(self):
        assert Vector.validate(1.0, float("nan")) is False

    def test_vector3_distance_to_self(self):
        vector3 = Vector3(1.0, 2.0, 3.0)

        assert isinstance(vector3, Vector3)
        assert vector3.distance_to(vector3) == 0.0

    def test_vector3_distance_to_other(self):
        vector3 = Vector3(1.0, 2.0, 3.0)
        other = Vector3(-4.0, -5.0, 6.0)

        # sqrt(25 + 49 + 9) = sqrt(83) ≈ 9.110
        assert vector3.distance_to(other) == pytest.approx(9.110, abs=0.001)

    def test_vector3_add_self(self):
        vector3 = Vector3(1.0, 2.0, 3.0)
        result = vector3.add(vector3)

        assert result.x == 2.0
        assert result.y == 4.0
        assert result.z == 6.0

    def test_vector3_validate_passes(self):
        assert Vector3.validate(1.0, 2.0, 3.0) is True

    def test_vector3_validate_fails(self):
        assert Vector3.validate(1.0, float("nan"), 3.0) is False

    def test_const_method(self):
        instance = StructWithConstMethod("")
        assert instance.double_const() == 0.0

    def test_static_methods_only(self):
        # Should run without raising.
        InterfaceStaticMethodsOnly.do_stuff()


class TestStructsWithConstants:
    def test_simple_route_default_description(self):
        assert SimpleRoute.DEFAULT_DESCRIPTION == "Nonsense"

    def test_simple_route_default_type(self):
        assert SimpleRoute.DEFAULT_TYPE == RouteType.EQUESTRIAN

    def test_simple_route_get_default_description(self):
        assert SimpleRoute.get_default_description() == "Nonsense"

    def test_multi_route_default_description(self):
        assert MultiRoute.DEFAULT_DESCRIPTION == "Foo"

    def test_multi_route_default_type(self):
        assert MultiRoute.DEFAULT_TYPE == RouteType.NONE

    def test_multi_route_get_default_description(self):
        assert MultiRoute.get_default_description() == "Foo"
