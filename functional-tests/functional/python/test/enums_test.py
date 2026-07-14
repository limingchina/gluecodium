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

"""Enum mapping tests for the Python (pybind11) bindings."""

import functional
from test.Enums import Enums
from test.EnumsTypeCollectionMethods import EnumsTypeCollectionMethods
from test.InternalError import InternalError
from test.InternalErrorTypeCollection import InternalErrorTypeCollection

import pytest


class TestEnums:
    def test_flip_enum_to_zero(self):
        result = Enums.flip_enum_value(InternalError.ERROR_FATAL)
        assert result == InternalError.ERROR_NONE

    def test_flip_enum_from_zero(self):
        result = Enums.flip_enum_value(InternalError.ERROR_NONE)
        assert result == InternalError.ERROR_FATAL

    def test_enum_members_exist(self):
        assert InternalError.ERROR_NONE is not None
        assert InternalError.ERROR_FATAL is not None

    def test_type_collection_enum_round_trip(self):
        result = EnumsTypeCollectionMethods.flip_enum_value(InternalErrorTypeCollection.ERROR_FATAL)
        assert result == InternalErrorTypeCollection.ERROR_NONE
