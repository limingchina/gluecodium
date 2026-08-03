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

"""Lambda (callback) tests for the Python (pybind11) bindings."""

from typing import Callable, Optional

from test.CallOverloadedLambda import CallOverloadedLambda
from test.ClassWithInternalLambda import ClassWithInternalLambda
from test.Lambdas import Lambdas
from test.LambdasDeclarationOrder import LambdasDeclarationOrder
from test.LambdasInterface import LambdasInterface
from test.LambdasWithStructuredTypes import LambdasWithStructuredTypes

TakeScreenshotCallback = LambdasInterface.TakeScreenshotCallback
LambdaHolder = Lambdas.LambdaHolder
ClassCallback = LambdasWithStructuredTypes.ClassCallback
StructCallback = LambdasWithStructuredTypes.StructCallback
SomeCallback = LambdasDeclarationOrder.SomeCallback
SomeStruct = LambdasDeclarationOrder.SomeStruct
from test.SignatureClashLambda import SignatureClashLambda
from test.StructWithLambda import StructWithLambda


class TestLambdas:
    def setup_method(self):
        Lambdas.reset_real_concatenator()

    def teardown_method(self):
        Lambdas.reset_real_concatenator()

    def test_concatenate(self):
        result = Lambdas.concatenate("a", "b", lambda first, second: f"{first}-{second}")

        assert result == "a-b"

    def test_get_concatenator(self):
        concatenator = Lambdas.get_concatenator("|")

        assert concatenator("a", "b") == "a|b"

    def test_compose_concatenators(self):
        concatenator = Lambdas.compose_concatenators(
            lambda first, second: f"{first}-{second}",
            lambda first, second: f"{first}|{second}",
        )

        assert concatenator("a", "b", "c") == "a-b|c"

    def test_concatenate_list(self):
        result = Lambdas.concatenate_list(
            ["a", "b", "c"],
            [lambda first, second: f"{first}-{second}", lambda first, second: f"{first}|{second}"],
        )

        assert result == "a-b|c"

    def test_static_lambda_property(self):
        Lambdas.real_concatenator_set(lambda first, second: f"{first}:{second}")

        assert Lambdas.real_concatenator()("a", "b") == "a:b"

    # --- G2: Nullable lambdas ---

    def test_get_concatenator_or_null_with_value(self):
        concatenator = Lambdas.get_concatenator_or_null(">.<")

        assert concatenator is not None
        assert concatenator("foo", "bar") == "foo>.<bar"

    def test_get_concatenator_or_null_with_null(self):
        result = Lambdas.get_concatenator_or_null(None)

        assert result is None

    def test_concatenate_or_not_with_callable(self):
        result = Lambdas.concatenate_or_not("foo", "bar", lambda first, second: f"{first}>.<{second}")

        assert result == "foo>.<bar"

    def test_concatenate_or_not_with_null(self):
        result = Lambdas.concatenate_or_not("foo", "bar", None)

        assert result is None

    def test_get_nullable_confuser_with_value(self):
        confuser = Lambdas.get_nullable_confuser()

        producer = confuser("foo")

        assert producer is not None
        assert producer() == "foo"

    def test_get_nullable_confuser_with_null(self):
        confuser = Lambdas.get_nullable_confuser()

        result = confuser(None)

        assert result is None

    def test_apply_nullable_confuser_with_value(self):
        def confuser(value):
            if value is not None:
                return lambda: value
            return None

        producer = Lambdas.apply_nullable_confuser(confuser, "foo")

        assert producer is not None
        assert producer() == "foo"

    def test_apply_nullable_confuser_with_null(self):
        def confuser(value):
            if value is not None:
                return lambda: value
            return None

        result = Lambdas.apply_nullable_confuser(confuser, None)

        assert result is None

    # --- Lambda as struct field / nested lambda in struct ---

    def test_cpp_lambda_in_struct(self):
        holder = Lambdas.get_concatenator_in_struct(">.<")
        result = holder.concatenator("foo", "bar")

        assert result == "foo>.<bar"

    def test_python_lambda_in_struct(self):
        delimiter = ">.<"
        concatenator = lambda first, second: f"{first}{delimiter}{second}"
        holder = LambdaHolder(concatenator)
        result = Lambdas.concatenate_in_struct("foo", "bar", holder)

        assert result == "foo>.<bar"

    def test_python_lambda_for_nested_struct_lambda(self):
        result = StructWithLambda.invoke_callback(lambda arg: arg)

        assert result == "some callback argument"

    # --- G4: Lambda on interface methods + lambda params/returns that are wrapper types ---

    def test_lambdas_interface_subclass(self):
        """LambdasInterface (an interface with a lambda-typed method) can be subclassed
        and instantiated from Python — verifies the pybind11 trampoline is constructible."""
        class _ScreenshotImpl(LambdasInterface):
            def __init__(self):
                super().__init__()
                self.received_callback = None

            def take_screenshot(self, callback):
                self.received_callback = callback

        impl = _ScreenshotImpl()
        assert impl.received_callback is None

    def test_lambdas_interface_take_screenshot_callback_type(self):
        """The TakeScreenshotCallback type alias maps Blob? to Optional[bytes]."""
        assert TakeScreenshotCallback == Callable[[Optional[bytes]], None]

    def test_lambdas_interface_take_screenshot_invocation(self):
        """Calling take_screenshot on a Python subclass delivers the callback and it can
        be invoked with bytes (Blob) and None (null Blob)."""
        class _ScreenshotImpl(LambdasInterface):
            def __init__(self):
                super().__init__()
                self.received_callback = None

            def take_screenshot(self, callback):
                self.received_callback = callback

        impl = _ScreenshotImpl()
        captured = []
        test_callback = lambda blob: captured.append(blob)
        impl.take_screenshot(test_callback)

        assert impl.received_callback is test_callback

        # The callback should accept bytes (Blob value) and None (null Blob)
        impl.received_callback(b"\x01\x02\x03")
        impl.received_callback(None)

        assert captured == [b"\x01\x02\x03", None]

    def test_lambdas_with_structured_types_callback_type_aliases(self):
        """LambdasWithStructuredTypes defines lambdas whose parameter types are wrapper
        types (interface and struct). Verify the generated type aliases are correct."""
        assert ClassCallback == Callable[[LambdasInterface], None]
        assert StructCallback == Callable[[LambdaHolder], None]

    # --- G5: @Overloaded lambda + composition regression ---

    def test_invoke_overloaded_lambda(self):
        """CallOverloadedLambda.invoke_overloaded_lambda exercises a @Overloaded lambda
        type (Int -> String) passed from Python into C++ and back."""
        result = CallOverloadedLambda.invoke_overloaded_lambda(lambda value: f"val={value}", 42)

        assert result == "val=42"

    # --- G6: @Internal lambda + doc comments (verification) ---

    def test_invoke_internal_lambda(self):
        """ClassWithInternalLambda.invoke_internal_lambda is an @Internal method
        that should NOT be exposed in the Python API.
        Verifies @Internal filtering removes the method from the Python binding."""
        assert not hasattr(ClassWithInternalLambda, "invoke_internal_lambda")

    # --- G7: LambdasDeclarationOrder + SignatureClashLambda regression ---

    def test_declaration_order_struct(self):
        """LambdasDeclarationOrder declares a lambda (SomeCallback) that references
        SomeStruct *before* the struct is declared. Verify the generated struct is
        usable and its field round-trips correctly."""
        struct = SomeStruct()
        struct.some_field = "order-test"

        assert struct.some_field == "order-test"

    def test_declaration_order_callback_type_alias(self):
        """The SomeCallback type alias references SomeStruct (declared after the lambda).
        Verify the generated type alias is correct."""
        assert SomeCallback == Callable[[SomeStruct], None]

    def test_signature_clash_lambda_type_alias(self):
        """SignatureClashLambda is a top-level lambda () -> String with a name that
        could clash with generated helper symbols. Verify it is a correct type alias."""
        assert SignatureClashLambda == Callable[[], str]
