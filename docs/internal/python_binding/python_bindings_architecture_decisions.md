# Python binding architecture decisions

These records describe accepted choices reflected in the current implementation.
They consolidate rationale from retired development plans and subsequent review
fixes; they do not assign retrospective approval dates. For usage and requirements,
see [Python bindings](../../python_bindings.md); for implementation and verification,
see the [development overview](README.md).

Examples using Calculator refer to the maintained sample. Other API names, such
as `Item`, `Shape` and `Point`, illustrate the decision rather than describe
additional built-in APIs. Snippets assume their generated types and application
objects are available.

## ADR 1: Compile generated pybind11 bindings alongside the C++ API

**Status:** Accepted.

**Context:** The Python boundary must support shared C++ objects, value types,
callbacks, collections and errors. A C ABI with ctypes/cffi would require a separate
ownership and callback-marshalling layer.

**Choice:** Generate pybind11 registration sources together with public Python
wrappers and stubs, using the existing C++ generator's API and runtime. The
application implements the C++ API and links it into a CPython extension.

**Consequences:** pybind11 supplies native type registration and base conversion;
Gluecodium supplies the public conversion, identity and GIL policies. The build
requires C++17, Python development headers and pybind11 3.1.0+. The wrapper layer
requires Python 3.10+. Extensions are tied to their Python ABI/platform. The native Calculator
example has been validated with Python 3.14 and pybind11 3.1.0 on Linux; this does
not establish free-threaded, subinterpreter or cross-platform validation.

**Example:** Generate the Calculator API with
`-generators cpp,python -pythonmodule calculator`, then compile the generated
pybind11 sources together with the C++ implementation into the `calculator`
extension. The public wrapper can then call that implementation:

```python
from gluecodium.calculator.Calculator import Calculator

calc = Calculator.make()
assert calc.summarize(2, 3) == 5
```

The extension supplies the native implementation; the generated Python package
supplies the public `Calculator` type used by the application.

**Implementation:** [PythonGenerator](../../../gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGenerator.kt),
[pybind11 templates](../../../gluecodium/src/main/resources/templates/python/).

## ADR 2: Use one public module per top-level element and physical nested types

**Status:** Accepted.

**Context:** A LIME file can contain multiple top-level elements. Flat nested-type
names followed by assignments obscure Python qualified names and static typing.

**Choice:** Emit `.py` and `.pyi` modules per top-level element under its LIME
package, with physically nested public classes. Render nested template bodies and
indent them in the generator. Keep package-qualified registration identifiers for
native top-level types, nested native scopes for nested types, and distinct native
extension and public package names.

**Consequences:** Public names and nested type-checker access remain natural.
Native registration names are implementation details. Explicit Python names take
precedence over naming rules; internal names use underscore conventions rather
than access enforcement. Parsed package override options currently do not relocate
wrapper output. Lazy imports/hint resolution reduce import cycles; arbitrary import
graphs and multiple independently generated runtimes still need dedicated coverage.

**Example:** The Calculator's LIME package `gluecodium.calculator` produces
`gluecodium/calculator/Calculator.py` and a matching `Calculator.pyi`.
Its nested `DivideArguments` struct is defined inside the public `Calculator`
class, so application code uses:

```python
from gluecodium.calculator.Calculator import Calculator

args = Calculator.DivideArguments(12, 3)
assert Calculator.DivideArguments.__qualname__ == "Calculator.DivideArguments"
```

The extension's package-qualified registration name,
`calculator.gluecodium_calculator_Calculator`, stays behind the public wrapper.

**Implementation:** [PythonGenerator](../../../gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGenerator.kt),
[PythonFile](../../../gluecodium/src/main/resources/templates/python/PythonFile.mustache),
[Pybind11File](../../../gluecodium/src/main/resources/templates/python/Pybind11File.mustache).

## ADR 3: Present one public conversion contract in both call directions

**Status:** Accepted.

**Context:** Native pybind11 objects and public wrappers are different Python
types. Callbacks should receive the same public Python types that the type hints
describe and regular methods return.

**Choice:** Recursively wrap/unwrap values for methods, properties, collections,
nullable values and callables. Install hidden, lazily resolved callback bridges
for generated interface subclasses, leaving direct Python calls to user overrides
with ordinary Python behavior. Preserve keyword arguments in native overload
forwarding rather than duplicating pybind11 dispatch in Python.

**Consequences:** Callback implementations use public types. Hint/import planning
must cover inherited and nested signatures. Overload resolution still belongs to
pybind11, so mixed argument forms and heterogeneous result shapes require explicit
tests. `None` must be handled before constructing an optional wrapper.

**Example:** Suppose an API exposes `Service.get_item() -> Item` and
`Observer.on_item(item: Item) -> None`, where `Item` is the generated public
wrapper. These are Python type hints: `-> Item` describes the method's result,
and `item: Item` describes the callback's argument. Both promise the same public
type:

```python
item = service.get_item()
assert isinstance(item, Item)

class MyObserver(Observer):
    def on_item(self, item: Item) -> None:
        assert isinstance(item, Item)
```

An ordinary method result is wrapped before it reaches the caller. A C++ callback
initially supplies a native pybind11 object, whose Python class differs from
`Item`. Passing it straight to the user override would make the second assertion
fail. The hidden callback bridge applies `_wrap(native_item, Item)` first, so both
assertions pass. Type hints alone do not perform this conversion. If a callback
returns an `Item`, the bridge applies `_unwrap()` before handing it back to
pybind11. The same conversion applies to items inside collections and optional
values.

**Implementation:** [PythonNativeBase](../../../gluecodium/src/main/resources/templates/python/PythonNativeBase.mustache),
[PythonFunction](../../../gluecodium/src/main/resources/templates/python/PythonFunction.mustache),
[trampoline functions](../../../gluecodium/src/main/resources/templates/python/Pybind11TrampolineFunction.mustache).

## ADR 4: Canonical dynamic identity with a weak public wrapper cache

**Status:** Accepted.

**Context:** A pointer-only strong cache both retained native ownership indefinitely
and let the first requested parent type determine later child results. Base pointers
can also differ for one multiply inherited object.

**Choice:** Normalize polymorphic native identity to the most-derived object;
select the most-specific bound public wrapper before caching. Regular views share
one weak cache entry. Deliberately narrow interfaces retain their declared view
and use separate entries. Resolve registry types lazily.

**Consequences:** Parent-first and child-first regular views agree while a wrapper
is alive. Weak entries do not keep native resources alive. If C++ retains an object
after its public wrapper dies, a later return creates a new wrapper; identity is
not promised across that lifetime gap. Expired entries cannot return wrappers for
reused addresses. Narrow views intentionally differ. A per-type key alone was
insufficient because it would sacrifice regular cross-view identity.

**Example:** Suppose `get_shape()` is declared to return `Shape` and
`get_circle()` is declared to return its bound subclass `Circle`. Both native
methods return the same C++ object:

```python
shape = service.get_shape()
circle = service.get_circle()
assert isinstance(shape, Circle)
assert shape is circle
```

Selecting the most-specific wrapper before caching makes this work even when the
base-typed method is called first. Once both public references are dropped, the
weak cache can discard the wrapper. If C++ still owns the object, a later call
creates a new wrapper. A deliberately narrow interface view has its own entry.

**Implementation:** [PythonNativeBase](../../../gluecodium/src/main/resources/templates/python/PythonNativeBase.mustache),
[native class identity/downcasts](../../../gluecodium/src/main/resources/templates/python/Pybind11Class.mustache).

## ADR 5: Keep callback ownership separate from wrapper caching

**Status:** Accepted.

**Context:** Removing cache retention must not imply that native shared ownership
keeps Python interface subclasses alive or that workers may outlive the interpreter.

**Choice:** Use the current shared-pointer/trampoline model and require applications
to retain Python interface owners until callbacks finish. A retained native
`std::function` retains its Python callable until native code releases the function.
Join or drain workers before releasing owners or shutting down Python.

**Consequences:** The weak cache is an identity facility, not an ownership substitute.
No smart-holder migration is claimed. Callback exception capture, worker cleanup
and shutdown order remain native application responsibilities. Generated GIL scopes
cannot repair native lock cycles or unsafe interpreter-finalization behavior.

**Example:** For an illustrative asynchronous service with `start(observer)`
and `join()`, retain the Python observer until `join()` has waited for every
callback-producing worker to finish:

```python
observer = MyObserver()
service.start(observer)
try:
    do_other_work()
finally:
    service.join()
del observer
```

The local `observer` reference keeps the Python subclass alive during callbacks.
The wrapper cache's weak reference cannot do that, and retaining only the native
C++ interface pointer does not establish the Python subclass's lifetime.

## ADR 6: Release the GIL around native work, preserve it around Python work

**Status:** Accepted.

**Context:** A caller holding the GIL while joining a worker that invokes Python
can deadlock. Blanket release around Python conversion or holder destruction is
also unsafe.

**Choice:** Release around real native methods/factories/accessors and exported
native callable invocation; acquire before overrides. Keep argument/result casts,
Python object management, plain struct field access and value construction under
the GIL. Use scoped native-call helpers for custom conversion branches and safe
callable export recursively through optional/collection/Return paths.

**Consequences:** Native calls can run concurrently and implementations must
synchronize their state. Callback exceptions must be captured and propagated after
workers join, not escape `noexcept` callbacks. Bounded subprocess tests are needed
to catch deadlocks and shutdown failures. Ordinary GIL-enabled CPython coverage does
not establish support for free-threaded builds.

**Example:** Suppose a native `run_and_join(callback)` method starts a worker
that calls Python, then waits for that worker. The generated boundary permits this
sequence:

```text
Caller: release the GIL, enter run_and_join(), wait for the worker.
Worker: acquire the GIL, invoke the Python callback, release the GIL, finish.
Caller: finish the native call, reacquire the GIL, convert the result.
```

If the caller kept the GIL while waiting, the worker could not acquire it to run
the callback, so neither thread could finish. Argument and result conversion
still run with the GIL held because they access Python objects.

**Implementation:** [Pybind11Function](../../../gluecodium/src/main/resources/templates/python/Pybind11Function.mustache),
[generic conversion helper](../../../gluecodium/src/main/resources/templates/python/Pybind11GenericCaster.mustache),
[trampoline properties](../../../gluecodium/src/main/resources/templates/python/Pybind11TrampolineProperty.mustache).

## ADR 7: Mutable value structs are unhashable; keys are immutable snapshots

**Status:** Accepted.

**Context:** Changing a value-based hash after dictionary/set insertion corrupts
lookup. Merely making the native transport unhashable would prevent pybind11 from
constructing raw collection keys before public wrapping.

**Choice:** Public mutable equatable structs are unhashable. Deeply immutable
value graphs retain value hashing. `as_key()` creates a frozen public subtype
owning a native struct copy; its accessors/methods operate on detached copies.
Native returned map/set keys are wrapped as snapshots. Private native structs use
identity equality/hash for transport, with explicit helpers for public value
comparison and hashing. Collection key conversion uses immutable representations.

**Consequences:** Mutating the original cannot affect a snapshot key. Equal public
values compare consistently; snapshot hashes remain stable. Shared mutable
value-equatable class/interface references and shared blobs cannot be isolated by
a struct copy and are rejected for snapshots. Public clients should use `as_key()`
when supplying mutable structs as keys; private native identity semantics are not
public value semantics.

**Example:** For a mutable equatable `Point` struct with scalar `x` and `y`
fields, create a snapshot before using its value as a dictionary key:

```python
point = Point(1, 2)
key = point.as_key()
values = {key: "saved"}

point.x = 9
assert values[Point(1, 2).as_key()] == "saved"
```

The stored key still represents `(1, 2)`; changing the original point cannot
change its hash. Using `point` itself as a key raises `TypeError`, and assigning
to `key.x` raises `AttributeError`. Private native struct objects remain usable
as transport keys before the public snapshot conversion.

**Implementation:** [PythonStruct](../../../gluecodium/src/main/resources/templates/python/PythonStruct.mustache),
[Pybind11Struct](../../../gluecodium/src/main/resources/templates/python/Pybind11Struct.mustache),
[PythonNativeBase](../../../gluecodium/src/main/resources/templates/python/PythonNativeBase.mustache).

## ADR 8: Model stubs after accessible runtime APIs and test consumers

**Status:** Accepted.

**Context:** Parsing a stub does not prove inherited members or usable constructor
calls type-check. Broad `*args, **kwargs` fallbacks hide invalid public calls.

**Choice:** Emit public interface bases in stubs and typed struct constructor
signatures derived from the retained native construction model. Omit inaccessible
native overloads; represent no-public-constructor cases so implicit object
construction is not falsely accepted. Give frozen key snapshots a typed subtype.
Test positive and negative consumer programs with mypy in addition to syntax checks.

**Consequences:** Stub inheritance is a static contract; adding bases to runtime
Python classes would require a separate design for pybind11 metaclasses and
Python's method resolution order. Keep native constructor changes, visibility,
defaults and stubs coordinated. Packaging typing markers and clean wheel
installation remain separate distribution work.

**Example:** A simplified stub for the Calculator's nested argument struct
declares its usable constructor:

```python
class Calculator:
    class DivideArguments:
        def __init__(self, dividend: int, divider: int) -> None: ...
```

A consumer check should accept `Calculator.DivideArguments(12, 3)` and reject
`Calculator.DivideArguments("twelve", 3)`. Parsing the stub alone cannot detect
an invalid constructor call in a consumer. Similarly, declaring
`Child(Parent)` in a stub lets a type checker find inherited members; it does not
change the runtime class's bases. Python's method resolution order is the order
in which a class and its bases are searched for attributes, so changing runtime
bases requires separate validation.

**Implementation:** [stub templates](../../../gluecodium/src/main/resources/templates/python/).

## ADR 9: Reuse chrono casters and adapt Gluecodium Return errors

**Status:** Accepted.

**Context:** Gluecodium `Return<Value, Error>` needs custom error conversion;
standard chrono types already have pybind11 casters. Early standalone spikes
established feasibility; the accepted implementation uses reusable generated casters.

**Choice:** Include `pybind11/chrono.h`. `Date` maps from
`std::chrono::system_clock::time_point` to pybind11's naive **local-time** datetime,
not a timezone-aware UTC datetime. `Duration` uses `std::chrono::seconds` and
`datetime.timedelta`; fractional precision is not guaranteed. For successful Return values, use guarded regular conversion helpers for
callable, optional and collection values; other values use
`type_caster<Value>::cast`, preserving the return policy and parent handle.
Successful `Void` maps to `None`. Failures use registered exception mapping with
`RuntimeError` fallback.

**Consequences:** Timezone and precision behavior must be understood by callers.
A custom UTC caster is not part of the accepted implementation. Enum-backed errors
share a C++ `std::error_code` registry entry, limiting distinction among multiple
enum error definitions. Payload exceptions carry messages rather than all original
fields. Do not infer a reverse Python-exception-to-Return contract without tests.

**Example:** The Calculator's C++ `summarize` method returns a Gluecodium
`Return`: success becomes an ordinary Python integer, while overflow raises
the registered native exception:

```python
import calculator as native
from gluecodium.calculator.Calculator import Calculator

calc = Calculator.make()
assert calc.summarize(2, 3) == 5
try:
    calc.summarize(2_000_000_000, 2_000_000_000)
except native.gluecodium_calculator_Calculator.CalculatorExceptionError as error:
    print(str(error))
```

For chrono values, `std::chrono::seconds{90}` becomes
`datetime.timedelta(seconds=90)`. A returned system-clock time point becomes a
naive local-time `datetime`, so callers must not interpret it as an explicitly
UTC-tagged value.

**Implementation:** [Pybind11File](../../../gluecodium/src/main/resources/templates/python/Pybind11File.mustache),
[Return caster](../../../gluecodium/src/main/resources/templates/python/Pybind11ReturnCaster.mustache).

## ADR 10: Separate generation/build integration from application packaging

**Status:** Accepted.

**Context:** The extension target needs generated sources before its initial
configuration; a complete distribution also needs implementation/runtime sources
and public packages.

**Choice:** Use the CMake helper and maintained Calculator example for integration.
Generate before configuring the extension target and reconfigure when source lists
change. Treat generated setuptools files as application-specific starting points.
Use smoke comparisons plus a real native functional build and consumer typing gate
in CI.

**Consequences:** Install the extension, wrappers and stubs together. The helper
builds an extension rather than a complete installed package. Fresh wheel installs,
PEP 561 metadata and broader platform/minimum-version coverage remain work to
validate. Async/asyncio support and effective package override options are not
established by synchronous functional tests.

**Example:** A Calculator installation for Linux and CPython 3.14 could contain
the following files; the extension suffix varies by interpreter and platform:

```text
site-packages/
  calculator.cpython-314-x86_64-linux-gnu.so
  _native_base.py
  gluecodium/
    __init__.py
    calculator/
      __init__.py
      Calculator.py
      Calculator.pyi
```

Building or copying only the extension does not supply the public
`from gluecodium.calculator.Calculator import Calculator` import. A complete
distribution must include the wrapper packages and stubs as well. The generated
`setup.py` must also be configured to compile or link the application's C++
implementation and generated runtime sources.

**Evidence:** [Calculator example](../../../examples/calculator/python/README.md),
[CMake helper](../../../cmake/modules/gluecodium/Python.cmake).
