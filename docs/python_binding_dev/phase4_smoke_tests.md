# Phase 4 — Smoke Tests for Implemented Features

> **Status**: ✅ Completed & committed (`python_bind` branch, commit `5ddfc38d7`)
> **Date**: 2026-07-13
> **Source plan**: `docs/python_pybind11_plan.md` (Phases 1–4)
> **Build**: `./gradlew :gluecodium:test --tests "com.here.gluecodium.SmokeTest"` → **success**
> (43 python smoke tests run, 5 skipped, 0 failed)

## Goal

Add smoke-test coverage for the Python/pybind11 generator so that the implemented features
(Phases 1–4) are locked by reference output and any future regression in the generator is caught
by `SmokeTest.kt`. The smoke tests follow the existing convention described in
`docs/internal/testing.md`: each feature's reference output lives under
`<feature>/output/<generator-name>/`, and the harness runs every registered generator against
every feature.

## Key structural decision: pybind11 output lives under `python/`

The `SmokeTest` harness recursively scans `<feature>/output/python/` for reference files. The
Python generator emits **two** kinds of files — `.py` (Python wrappers) and `.cpp`/`.h`
(pybind11 bindings). To make both discoverable by the harness, the pybind11 target directory was
changed to be nested under the Python target directory:

**`gluecodium/.../generator/python/PythonNameRules.kt`**
```kotlin
val PYTHON_TARGET_DIRECTORY = "python" + File.separator
val PYBIND11_TARGET_DIRECTORY = PYTHON_TARGET_DIRECTORY + "pybind11" + File.separator
```

So a generated feature now produces:
```
<feature>/output/python/
├── __init__.py
├── <package>/.../*.py          # Python wrappers
└── pybind11/                   # pybind11 C++ bindings (nested under python/)
    ├── _return_caster.h
    └── <package>_<Name>.cpp
```

Without this nesting, the `.cpp` reference files would be placed in a sibling `pybind11/`
directory that the harness never inspects, so binding regressions would go undetected.

## Coverage

### Existing features (bulk-generated reference output)

For every existing smoke feature whose LIME model parses successfully, `python/` + `python/pybind11/`
reference output was generated with the same options the harness applies (the per-feature
`commandlineoptions.txt` is honoured, substituting `$INPUT_FOLDER`/`$AUX_FOLDER`; the harness
`TEST_OPTIONS` `cppInternalNamespace = ["gluecodium"]` and `internalPrefix = "foobar_"` are
replicated via `-intnamespace gluecodium -internalprefix foobar_`).

This exercises, across the implemented phases:
- **Phase 1** — `@Python(Name/Skip/Internal)` attribute filtering (verified by the dedicated
  `python_attributes` feature below, and also present in features using `@Skip`/`@Internal`).
- **Phase 3** — per-type templates: class / interface / struct / enum / exception / lambda /
  typealias wrappers and their `register_*` pybind11 bindings.
- **Phase 4** — type mapping: basic types, `Date`/`Duration`/`Locale`, nullable (`Optional[T]`),
  containers (`list`/`set`/`dict`), and the generated `pybind11/_return_caster.h` for
  `Return<T, Error>`.

Features covered include (non-exhaustive): `basic_types`, `structs`, `enums`, `errors`,
`attributes`, `properties`, `inheritance`, `multiple_inheritance`, `listeners`, `lambdas`,
`nullable`, `dates`, `durations`, `locales`, `external_types`, `skip`, `name_rules`,
`namespace_basic`, `visibility_attribute`, `visibility_platform`, `defaults`, `defaults_const`,
`field_constructors`, `constructors`, `constants`, `escaped_names`, `expose_internals`,
`internal_fields`, `nesting`, `packages`, `platform_names`, `serialization`, `typedefs`,
`async`, `equatable`, `declaration_order`, `duplicate_names`, `full_name`, `instances`,
`method_overloads`, `no_cache`, `throwing_constructors`, `annotations`, `comments`-adjacent
naming-rule features, etc.

### Dedicated `python_attributes` feature (Phase 1 attribute)

A new feature `gluecodium/src/test/resources/smoke/python_attributes/` was added to specifically
exercise the `@Python` attribute introduced in Phase 1:

```lime
@Python(Name = "RenamedClass")
class MyClass {
    @Python(Skip)
    fun hiddenMethod(): Void

    @Python(Internal)
    fun internalMethod(): String

    fun visibleMethod(param: Int): String
}

@Python(Skip)
class SkippedClass {
    fun wontBeGenerated(): Void
}
```

Expected (and verified) behaviour:
- `MyClass` is generated as `RenamedClass.py` — the `@Python(Name = ...)` override is honoured.
- `SkippedClass` and `MyClass.hiddenMethod` are **not** generated (Python-side filtering via
  `LimeModelSkipPredicates` + `PYTHON` attribute).
- `MyClass.internalMethod` is retained (it is `@Python(Internal)`, not `@Python(Skip)`).

## Features intentionally without Python output (skipped by harness)

The harness skips a feature for a generator when `<feature>/output/python/` has no reference
files. The following are intentionally left without Python output:

- **`comments`** and **`generic_types`** — these LIME files fail to *parse* for **all**
  generators (not python-specific; `cpp` fails identically). The harness cannot load the model,
  so the python test case is skipped. No reference output is committed.
- **`name_clash_overloads`** — a python-specific limitation: two LIME types resolve to the same
  Python file name (`AssetsManager.py`), causing a generator filename collision
  (`checkForFileNameCollisions`). This is a known edge case tracked for later; no python output
  is committed so the harness skips it.
- **`strict_fail_immutable`** / **`strict_fail_internal`** — these are intentional *validation*
  failures (each has a `validationfail.txt`); the harness expects validation to fail and produces
  no output. No python reference output is committed.

## How to regenerate / update

To refresh the reference output after a generator change, run the generator over each feature's
input with the harness options and copy `python/` into `output/python/`. The one-shot command used
here (applies each feature's `commandlineoptions.txt` and the harness `TEST_OPTIONS`):

```bash
GLUE=./gluecodium/build/install/gluecodium/bin/gluecodium
SMOKE=gluecodium/src/test/resources/smoke
for d in "$SMOKE"/*/; do
  [ -d "$d/input" ] || continue
  co="$d/input/commandlineoptions.txt"
  inp=$(dirname "$co"); aux="$d/auxiliary"; [ -d "$aux" ] || aux="$inp"
  out=$(mktemp -d); optsfile=$(mktemp)
  if [ -f "$co" ]; then
    sed "s|\$INPUT_FOLDER|$inp|g; s|\$AUX_FOLDER|$aux|g" "$co" > "$optsfile"
    "$GLUE" $(cat "$optsfile") -generators python -output "$out"
  else
    "$GLUE" -input "$inp" -generators python -intnamespace gluecodium \
            -internalprefix foobar_ -output "$out"
  fi
  [ -d "$out/python" ] && { rm -rf "$d/output/python"; mkdir -p "$d/output/python"; \
                            cp -r "$out/python/." "$d/output/python/"; }
  rm -rf "$out" "$optsfile"
done
```

Alternatively, the built-in dump mechanism regenerates *all* generators at once:
`DUMP_ACTUAL_DIR=$(pwd)/gluecodium/src/test/resources/smoke ./gradlew test`
(then review the diff before committing — note this also rewrites non-python output).

### ⚠️ `name_clash_overloads` must stay skipped

The bulk loop above will create `name_clash_overloads/output/python/` because two LIME types
in that feature resolve to the same Python file name `AssetsManager.py` and the generator
throws a filename-collision error. Committing that output makes the `python` `SmokeTest` case
**fail** on the next run (`executeGenerator` returns false). This is a known, expected skip —
**delete the directory after regenerating** and do not commit it:

```bash
rm -rf gluecodium/src/test/resources/smoke/name_clash_overloads/output/python
```

(The other skipped features — `comments`, `generic_types`, `strict_fail_immutable`,
`strict_fail_internal` — are skipped for non-python reasons and also have no `output/python/`.)
See `docs/python_binding_dev/phase6_implementation.md` §4.1 for details.

## Verification

```
./gradlew :gluecodium:test --tests "com.here.gluecodium.SmokeTest"
# 288 tests, python: 43 run / 5 skipped / 0 failed
```

## Next step

Phase 5 (object lifecycle & callbacks) and Phase 6 (module init `PYBIND11_MODULE`, `.pyi` stubs)
are implemented by another session. Once Phase 6 wires the `register_*` functions into a module
entry point and includes `_return_caster.h`, the generated `.cpp` files become independently
compilable and **functional tests** (CMake + pybind11 build) can be added under
`functional-tests/`. Until then, only smoke tests are applicable.
