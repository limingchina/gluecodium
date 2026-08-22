# Phase 0 — Prerequisites Spike Results (WASM/embind Binding)

> **Status**: ✅ Complete — all three gates passed. **GO for Phase 1/2.**
> **Date**: 2026-08-22
> **Spike code**: `docs/wasm_binding_dev/spikes/mi_spike/` and `docs/wasm_binding_dev/spikes/emcmake_spike/`

---

## 0.1 Emscripten SDK version and toolchain shape — ✅ PASS

| Tool | Version |
|------|---------|
| `emcc`/`em++`/`emcmake` | **6.0.6-git** (Homebrew) |
| Node.js | v23.6.1 (nvm) |
| CMake | 4.3.1 |

- embind ships inside Emscripten (`<emscripten/bind.h>`) — no separate package, as planned.
- Plan recommended emsdk ≥ 3.1.51; 6.0.6 far exceeds it. `optional<T>`-era embind features and
  `WASM_BIGINT` are mature here.
- **⚠️ CMake version caveat**: CMake 4.3.1 emits a warning that emscripten *shared libraries* are
  only supported with cmake < 4.2.0 or > 4.3.3. The calculator example's `add_library(SHARED)`
  silently degrades to STATIC under emcmake. Harmless for our use (we link statically into the
  final wasm anyway), but `Js.cmake` (Phase 7) must not rely on shared-library semantics.

## 0.2 Multiple-inheritance spike — ✅ PASS (go)

**Code**: `spikes/mi_spike/mi_spike.cpp` + `test.js`, compiled with
`em++ -std=c++17 -lembind -fexceptions -sWASM_BIGINT=1 -sMODULARIZE=1`.

Mirrors `MultipleInheritance.lime` (`class MultiClass : OpenClass, NarrowInterface`). All checks passed:

1. **Primary base via `base<OpenClass>`** — inherited members (`parentFunction`, `parentProperty`)
   are visible and callable on the JS `MultiClass` wrapper. ✅
2. **Flattened secondary parent** — binding `NarrowInterface` members again against
   `MultiClass` member pointers works, and **virtual dispatch is correct**: the flattened
   `parentFunctionLight()` invoked the `MultiClass` override, not the base implementation. ✅
3. **Explicit upcast helper** (`upcastToNarrow` returning `NarrowInterface*` with
   `allow_raw_pointers()`) returns a usable JS object; virtual calls through the upcast view
   dispatch correctly. ✅
4. **Distinct C++ objects → distinct JS wrappers** (basic referential-identity sanity). ✅

**Conclusion**: the §5.3 mitigation (primary base + flattened secondary members + explicit upcast
helpers) is viable. Remaining Phase 5 follow-up: verify referential equality when the *same*
object is retrieved through both the primary and the upcast path (embind's internal pointer cache
behavior for raw-pointer returns needs a dedicated check — see §5.2 of the plan).

## 0.3 `emcmake` build of the calculator example — ✅ PASS (with findings)

**Code**: `spikes/emcmake_spike/`. Steps that worked:

```bash
GLUECODIUM_PATH=<repo> emcmake cmake -G Ninja -DENABLE_APP=OFF <repo>/examples/calculator -B build
cmake --build build   # gradle-run Gluecodium generates cpp; em++ compiles it cleanly
```

The **entire generated C++ output** (unity main/common glue, `Calculator.cpp`, `LocaleImpl.cpp`,
`TypeRepositoryImpl.cpp`) compiled under `em++` with **zero source changes** — no host-only
constructs, no RTTI/threading surprises. Then a hand-written `EMSCRIPTEN_BINDINGS` entry point
(`main.cpp`) over the generated headers produced a working `calculator.js` + `calculator.wasm`,
verified in Node (`summarize(2,3) = 5`).

### Findings that shape Phase 3/4 design

1. **`Return<T, E>` is not auto-convertible by embind** (confirmed empirically: binding
   `&Calculator::summarize` directly fails at runtime with
   `UnboundTypeError: ... unbound types: N10gluecodium6ReturnIiNSt3__210error_codeEEE`).
   The generator **must** emit custom type casters for `gluecodium::Return<T, std::error_code>`
   (map to JS value-or-throw), analogous to the Python plan's custom return-value policies.
   This is a *hard requirement*, not an optimization — add to Phase 4 alongside the
   `std::optional<T>` caster spike.
2. **`std::optional<T>` parameters/returns** appear pervasively even in the trivial calculator
   (`max`, `DivideResult` fields). Confirms the optional-caster spike is Phase-4-critical.
3. **Generated struct constructors** (`DivideArguments(dividend, divider)`,
   `DivideResult` with defaulted optional members) are embind-friendly — `value_object` or
   constructor binding will work, but field names must be resolved via the JS name resolver.
4. **Link requirements confirmed**: `-lembind -fexceptions -sWASM_BIGINT=1 -sMODULARIZE=1
   -sALLOW_MEMORY_GROWTH=1` all work as planned; the generated glue TUs must be linked together
   with the embind entry point into one binary (as §7 of the plan anticipates).
5. **Generation pipeline works under emcmake unchanged**: `GLUECODIUM_PATH` + the existing
   `gluecodium_generate()` CMake machinery ran the generator via Gradle inside an Emscripten
   toolchain configure with no modification. Phase 7's `Js.cmake` can reuse this path directly.

## Gate decision

| Gate | Result |
|------|--------|
| 0.1 Toolchain | ✅ emsdk 6.0.6, Node 23 |
| 0.2 Multiple inheritance | ✅ Mitigation works, virtual dispatch correct |
| 0.3 emcmake build | ✅ Generated C++ compiles clean; wasm runs in Node |

**Proceed to Phase 1** (LIME model layer: `@Js` attribute, converter, name rules, options/CLI).

### Carry-forward items for later phases
- Phase 4: custom `Return<T, E>` caster (new, from 0.3 finding #1) + `std::optional<T>` caster spike.
- Phase 5: verify same-object identity across primary-base and upcast retrieval paths.
- Phase 7: avoid shared-library semantics (CMake 4.3.1 limitation); static-link everything into one wasm.
