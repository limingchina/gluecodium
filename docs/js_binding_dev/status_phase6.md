# JavaScript/Embind Generator - Phase 6 Status

**Status**: Complete for generated output structure, TypeScript metadata, and ES-module package facades

**Date**: 2026-08-23

## Scope Delivered

Phase 6 completes the output structure required by the JavaScript/embind plan. The generator now
emits:

- one `.d.ts` declaration file per top-level LIME type under `js/<package>/`;
- one `index.d.ts` package entrypoint per LIME package;
- one executable `index.mjs` package facade per LIME package;
- `js/runtime.mjs`, which instantiates and wraps the Emscripten module once for all package facades;
- `js/package.json` with ESM package mode and an `exports` entry for every Lime package;
- `js/tsconfig.json` with strict TypeScript checking over generated declarations;
- one embind `.cpp` file per top-level LIME type under `js/embind/`;
- `js/embind/_module_init.cpp`, which registers generic types and invokes per-type registrations
  in dependency order; and
- `js/WrapperRuntime.mjs`, which remains the generated JavaScript lifecycle and wrapper-cache
  integration point from Phase 5.

The declaration index re-exports each top-level type with a relative declaration-module path. The
runtime index re-exports every bindable public type in the package, including nested types, by
mapping its public leaf name to a private embind runtime name derived from the canonical Lime path.
Package facades are the public JavaScript namespace; consumers do not access the raw Emscripten
module's private names directly.

## Generation Contract

Package indexes and TypeScript metadata are emitted when `jsEmitTypeScriptStubs` is enabled,
which is the default. Runtime package facades and `package.json` exports are emitted regardless,
so disabling declarations does not remove the executable ES-module API.

The generated `package.json` declares the package-relative TypeScript entrypoint when declarations
are enabled and maps each package subpath to both `index.d.ts` and `index.mjs`. It intentionally
does not expose a root runtime entry: package subpath imports are the namespace boundary, and all
of them share one Wasm module instance through `runtime.mjs`.

## Verification

The focused generator compilation passes:

```text
./gradlew :gluecodium:compileKotlin
BUILD SUCCESSFUL
```

The implementation is consumed by the Phase 7 calculator build and the Phase 8 Node.js functional
tests. The remaining declaration-side gap is strict TypeScript coverage for nested public types.