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

"""Call the C++ calculator through generated Python wrappers."""

import calculator as native
from com.example.calculator.Calculation import Calculation
from com.example.calculator.CalculationListener import CalculationListener
from com.example.calculator.Calculator import Calculator


class PrintingListener(CalculationListener):
    def __init__(self):
        super().__init__()
        self.results = []

    def on_calculated(self, result: Calculation) -> None:
        self.results.append(result.value)
        print(f"[listener] {result.expression} = {result.value}")


def main() -> None:
    calculator = Calculator.create()
    # Retain the Python subclass while C++ holds and invokes the listener.
    listener = PrintingListener()
    calculator.set_listener(listener)

    for operation, left, right in (
        (calculator.add, 2.0, 3.0),
        (calculator.subtract, 9.0, 4.0),
        (calculator.multiply, 6.0, 7.0),
        (calculator.divide, 12.0, 3.0),
    ):
        result = operation(left, right)
        print(f"result: {result.expression} = {result.value}")

    print("calculation_count ->", calculator.calculation_count)
    calculator.calculation_count = 0
    print("calculation_count after reset ->", calculator.calculation_count)

    try:
        calculator.divide(1.0, 0.0)
    except native.com_example_calculator_CalculatorErrorError as error:
        print("divide by zero ->", type(error).__name__)

    # A struct can also be constructed on the Python side.
    manual_result = Calculation("manual", 42.0)
    print("manual result ->", manual_result.expression, manual_result.value)


if __name__ == "__main__":
    main()
