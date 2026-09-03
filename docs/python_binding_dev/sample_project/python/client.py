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

"""End-to-end client for the Gluecodium-generated greeter bindings.

This script exercises the generated Python wrapper classes produced by
Gluecodium's `python` generator (which sit on top of the native pybind11
extension module). It demonstrates:

  * instantiating a generated class (`Greeter.create()`),
  * calling a method that returns a value,
  * handling a `throws` error (mapped to a Python exception),
  * implementing a generated `interface` from Python (the `GreetingListener`
    trampoline), and
  * reading/writing a generated `property`.

The generated `.py` wrapper classes are directly importable (each package
directory ships an `__init__.py`, the circular self-import is filtered out, and
the wrappers expose factory constructors), so this client drives the generated
`com.example.greeter.Greeter` Python class directly.
"""

from com.example.greeter.Greeter import Greeter
from com.example.greeter.Greeting import Greeting
from com.example.greeter.GreetingListener import GreetingListener


class PrintingListener(GreetingListener):
    """A Python implementation of the generated GreetingListener interface."""

    def __init__(self):
        super().__init__()
        self.received = []

    def on_greeting(self, value: str) -> None:
        self.received.append(value)
        print(f"[listener] {value}")


def main() -> None:
    greeter_obj = Greeter.create()
    print("Created:", greeter_obj)

    # A normal greeting returns a string.
    message = greeter_obj.greet("World")
    print("greet('World') ->", message)

    # Register a Python-side listener; the C++ implementation invokes it.
    listener = PrintingListener()
    greeter_obj.add_listener(listener)

    # Greeting again triggers the listener callback (GIL-safe trampoline).
    greeter_obj.greet("Ada")

    # The property reflects how many greetings were produced.
    print("greeting_count ->", greeter_obj.greeting_count)
    greeter_obj.greeting_count = 10
    print("greeting_count after set ->", greeter_obj.greeting_count)

    # An empty name triggers the `throws GreeterError` path, which the
    # generated caster raises as a Python exception.
    try:
        greeter_obj.greet("")
    except Exception as exc:  # noqa: BLE001 - demonstrating error mapping
        print("greet('') raised:", type(exc).__name__, "-", exc)

    # Structs are passed by copy and expose read/write fields.
    g = Greeting("Bob", 3)
    print("Greeting struct:", g.name, g.count)


if __name__ == "__main__":
    main()
