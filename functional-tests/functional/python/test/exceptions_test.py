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

"""Exception mapping tests for the Python (pybind11) bindings."""

import functional
from test.errors import Errors, WithPayloadError
from test.errors import Payload

import pytest


class TestExceptions:
    def test_method_with_error_throws(self):
        with pytest.raises(WithPayloadError) as exc_info:
            Errors.method_with_payload_error(True)
        assert exc_info.value.message is not None

    def test_method_with_error_does_not_throw(self):
        # Should return normally (no exception raised).
        Errors.method_with_payload_error(False)

    def test_method_with_payload_error_and_return_value(self):
        with pytest.raises(WithPayloadError):
            Errors.method_with_payload_error_and_return_value(True)
        # When the flag is false a string is returned instead of raising.
        result = Errors.method_with_payload_error_and_return_value(False)
        assert isinstance(result, str)
