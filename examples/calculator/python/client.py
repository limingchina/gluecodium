# Copyright (C) 2026 HERE Europe B.V.
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

"""Exercise the shared Calculator API through generated Python wrappers."""

import calculator as native
from gluecodium.calculator.Calculator import Calculator


class ResultCallback(Calculator.MultiplyCallback):
    def __init__(self):
        super().__init__()
        self.result: int | None = None
        self.error: Calculator.CalculatorError | None = None

    def on_result(self, result: int) -> None:
        self.result = result
        self.error = None
        print("multiply ->", result)

    def on_error(self, error: Calculator.CalculatorError) -> None:
        self.result = None
        self.error = error
        print("multiply error ->", error.name)


def main() -> None:
    calculator = Calculator.make()
    assert calculator.summarize(2, 3) == 5
    print("sum ->", calculator.summarize(2, 3))

    differences = []
    calculator.subtract(9, 4, lambda error, result: differences.append((error, result)))
    assert differences == [(None, 5)]
    print("subtract ->", differences[0][1])

    # Retain the Python interface owner while C++ invokes its methods.
    callback = ResultCallback()
    calculator.multiply(6, 7, callback)
    assert callback.result == 42 and callback.error is None
    calculator.multiply(2_000_000_000, 2, callback)
    assert callback.error == Calculator.CalculatorError.RESULT_OUT_OF_BOUNDS

    result = calculator.divide(Calculator.DivideArguments(12, 3))
    assert result.result == 4.0 and result.error is None
    print("divide ->", result.result)
    invalid = calculator.divide(Calculator.DivideArguments(1, 0))
    assert invalid.result is None and invalid.error == Calculator.CalculatorError.DIVIDE_BY_ZERO
    print("divide by zero ->", invalid.error.name)

    assert calculator.min(9, 4).get_result() == 4
    print("min ->", calculator.min(9, 4).get_result())
    assert calculator.max(None, 7) == 7
    assert calculator.max(3, 7) == 7
    assert calculator.max(None, None) is None
    print("max(None, 7) ->", calculator.max(None, 7))

    try:
        calculator.summarize(2_000_000_000, 2_000_000_000)
    except native.gluecodium_calculator_Calculator.CalculatorExceptionError as error:
        print("sum overflow ->", type(error).__name__)
    else:
        raise AssertionError("Expected an overflow exception")


if __name__ == "__main__":
    main()
