# Python binding review fixes

Branch: `python_bind`; PR: https://github.com/limingchina/gluecodium/pull/2

| Review finding | Status | Commit |
| --- | --- | --- |
| 1. Overload keyword forwarding | Fixed; 360 Python functional tests passed | ad469a14d31ccef8777a98ba6df162db1d5092db |
| 2. Canonical wrapper type and identity | Fixed; 365 functional / 923 Gradle cases passed | ed8771474fb32e3397f57001d87d5e34c7497934 |
| 3. Nullable uncached wrapper returns | Fixed; 375 functional tests passed; 3 old-code regressions reproduced | c2bb4b939e5e1ba9aae4db4f07201b49725ff7d7 |
| 4. Public callback conversions | Fixed: 399 functional tests each on Python 3.10 and 3.14; Gradle 923 cases, zero failures, 63 skipped; focused before/fixed probes verified | d7ddd1cd698f08f56bb7350b2512bb1b51095556 |
| 5. Mutable struct hashing | Fixed: 414 Python 3.14 functional tests passed; Gradle 923 cases, zero failures; snapshot typing and native map/set transport covered | 414822c425930ccb9b8517a131eb9b64db64723b |
| 6. Interface stub inheritance | Fixed: 415 Python 3.14 functional tests passed; full Gradle passed; genuine inherited API typing regression | 722d1437099276f9c588888176afa85414b8a40c |
| 7. Struct stub constructor signatures | Fixed: 417 Python 3.14 functional tests passed; full Gradle passed; typed public overloads and no-public-constructor rejection | 5277c3843630f3690677f1b59fac79a8c47fde0d |
| 8. Threaded callbacks and GIL | Fixed: 433 Python 3.14 functional tests, including 16 bounded threaded cases; Gradle 923 cases, zero failures, 63 skipped; original 20-second deadlock reproduced | 89625ee56b54d8f6866e57a1582aaa2c5b3c9ad6 |
| 9. Wrapper cache lifetime | Fixed: 446 Python 3.14 functional tests, including 13 lifetime cases; Gradle 923 cases, zero failures, 63 skipped; 11 old-cache retention failures reproduced | d3fd7543e07f3f6a97f69ce1e99b1b4cda968dfc |

Compiler cache: `/workspace/ccache-dist/ccache` version 4.14.1; cache `/workspace/ccache-cache`; C and C++ CMake launchers enabled; one repeated compilation verified a direct cache hit.

CI workflow: `0a6289376578602fa21e34787382f7dae42fec9f`; context fix: `bc0af6846ec47d18ed4e784b3fb6ed8d16b09d8e`. Python 3.14 and pybind11 3.1.0 pinned; actionlint 1.7.12 passes; GitHub Python workflow passed: https://github.com/limingchina/gluecodium/actions/runs/37229709316 (both generator smoke and native functional steps passed). Local Python 3.14.7 environment `/workspace/python314-venv`; native build `/workspace/python314-functional-build`.

Validation preference: per user, future builds and functional validation concentrate on Python 3.14 with pybind11 3.1.0. Issue #4 was also verified on Python 3.10.

Publication transport: fixes #7–9 were published through the GitHub connector with exact tested trees verified. Shell git authentication recovered on 2026-10-05; git fetch origin python_bind succeeded. Local python_bind and origin/python_bind now both point to d3fd7543e07f3f6a97f69ce1e99b1b4cda968dfc with the same tested tree and a clean working tree.

Latest completed pushed revision (#7): Python bindings CI run 37235265991 succeeded, including smoke and native functional steps; Unit and Functional workflows also succeeded.

Threading fix (#8) GitHub CI: Python run 37238281124, Unit, Functional, and MacOS workflows all succeeded.

All nine numbered review findings are fixed in separate signed-off commits and published to python_bind. Latest remote head: d3fd7543e07f3f6a97f69ce1e99b1b4cda968dfc; exact tested tree bfec7139616fdb918bcface7444bf195581676e2. Final local functional gate: 446 tests passed.

Final revision Python 3.14 / pybind11 3.1.0 GitHub CI passed both smoke and native functional steps: https://github.com/limingchina/gluecodium/actions/runs/37255059189 . Unit tests also passed. Other platform Functional and MacOS workflows remained in progress at this check.
