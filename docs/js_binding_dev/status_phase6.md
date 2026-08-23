# JavaScript/Embind Generator - Phase 6 Status

**Status**: Complete for generated output structure and TypeScript package metadata

**Date**: 2026-08-23

## Scope Delivered

Phase 6 completes the output structure required by the JavaScript/embind plan. The generator now
emits:

- one `.d.ts` declaration file per top-level LIME type under `js/<package>/`;
- one `index.d.ts` package entrypoint per LIME package;
- `js/package.json` with the generated module name and ESM package mode, plus a declaration
  entrypoint when the model contains exactly one LIME package;
- `js/tsconfig.json` with strict TypeScript checking over generated declarations;
- one embind `.cpp` file per top-level LIME type under `js/embind/`;
- `js/embind/_module_init.cpp`, which registers generic types and invokes per-type registrations
  in dependency order; and
- `js/WrapperRuntime.mjs`, which remains the generated JavaScript lifecycle and wrapper-cache
  integration point from Phase 5.

The package index re-exports each top-level type with a relative declaration-module path. Nested
types remain declared in their owning top-level file, so the index does not create duplicate
exports or additional public names.

## Generation Contract

Package indexes and TypeScript metadata are emitted when `jsEmitTypeScriptStubs` is enabled,
which is the default. When declaration generation is disabled, embind C++ output and the common
runtime files are still generated, but no declaration package is advertised.

The generated `package.json` is intentionally metadata-only at this stage. For a single LIME
package it declares the correct package-relative TypeScript entrypoint. For multiple LIME packages
it omits `types`, because there is no honest single root declaration entrypoint; each package's
`index.d.ts` remains directly usable. The descriptor does not claim a `main`, `module`, or
`exports` runtime entry because the Emscripten JavaScript/wasm module is produced by Phase 7 build
integration. This avoids promising a runtime file path before the CMake module and calculator
example establish that contract.

## Verification

The focused generator compilation passes:

```text
./gradlew :gluecodium:compileKotlin
BUILD SUCCESSFUL
```

The implementation is ready for Phase 7 to consume. Phase 8 still needs to add an executable
assertion that generates a representative package, runs `tsc --strict` using the emitted
`tsconfig.json`, and verifies the package index resolves every top-level declaration.