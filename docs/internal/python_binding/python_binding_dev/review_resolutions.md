# Python binding review resolutions

This record preserves regression evidence from the [original review](review_history.md).
The counts below describe validation at each fix, rather than a permanent suite size
or a current CI result. Current gates are defined by the checked-in tests and
[CI workflow](../../../../.github/workflows/python-bindings.yml). The fixes were developed
as separate changes; branch names and commit IDs from the old progress diary were
retired when the contribution history was rewritten for matching DCO signoffs.

| Finding | Resolution and regression evidence |
| --- | --- |
| 1. Overload keywords | Forward positional and keyword values through conversion; static, instance, constructor, mixed and invalid-argument tests. Functional gate: 360 tests. |
| 2. Wrapper type/identity | Canonical dynamic wrapper selection, normalized polymorphic identity, separate narrow views; parent-first/child-first and multiple-inheritance tests. Gate: 365 tests. |
| 3. Nullable returns | Union-aware conversion on cache misses; three old-code failures reproduced, `None` and cached/uncached returns covered. Gate: 375 tests. |
| 4. Callback types | Lazy public/native adapters for methods, properties and callables; inherited callable imports and nullable cases included. Gates: 399 tests on Python 3.10 and 3.14. |
| 5. Mutable hashing | Unhashable mutable value wrappers, frozen key snapshots, identity-based private native transport and typed snapshot consumers. Python 3.14 gate: 414 tests. |
| 6. Interface stubs | Public interface bases in stubs; genuine positive/negative mypy consumers for substitution and inherited members. Gate: 415 tests. |
| 7. Constructor stubs | Typed accessible native overloads, including partial/default construction; unavailable constructors rejected by typing and runtime probes. Gate: 417 tests. |
| 8. Threading/GIL | Native-work release scopes and safe callable export; original worker/join deadlock reproduced with a 20-second subprocess bound. Gate: 433 tests, including 16 bounded threaded cases. |
| 9. Cache lifetime | Weak canonical cache with native lifetime counters, pointer-reuse and callable-owner checks; 11 old-cache retention failures reproduced. Gate: 446 tests, including 13 lifetime cases. |

The final local native gate used Python 3.14 and pybind11 3.1.0 and passed 446 tests.
The final full Gradle gate reported 923 cases, zero failures and 63 skips.
[The recorded final Python CI run](https://github.com/limingchina/gluecodium/actions/runs/37255059189)
passed both generator smoke and native functional steps. These results apply to
that tested source tree and do not replace checks on subsequent changes.

The lifetime fix does not introduce `py::smart_holder` ownership for Python
interface subclasses. Keep their owners alive until native callbacks finish;
retained `std::function` callables have a separate ownership contract. See the
[architecture decisions](../../../python_bindings_architecture_decisions.md).
