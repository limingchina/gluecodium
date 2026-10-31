# Ruscodium execution tasks

This checklist executes the [plan](PLAN.md). Check items only after producing
the named behavior and verification. Keep deferred parity work visible instead
of marking the entire port complete after the preview.

## M0: planning and setup

- [x] Inspect upstream grammar, architecture, model resolution, validators,
  existing inputs, and C++ generation design.
- [x] Record the unavailable Claude share and use repository evidence.
- [x] Write `PLAN.md` and this file before adding implementation code.
- [x] Commit the plan/task baseline before implementation.
- [x] Establish a standalone Cargo library/binary under `ruscodium/` with a
  lockfile and local build-output ignore rules.

## M1: frontend

- [ ] Source files, byte spans, line/column diagnostics and structured errors.
- [ ] Lexer: newline-aware tokens, comments, backticks, strings/multiline
  strings, escapes, signed numeric/special/duration forms.
- [ ] Model types retaining declarations, attributes, documents, descriptors,
  literal expressions, and type-reference structure.
- [ ] Parser: packages/imports, classes/interfaces/inheritance, structs, fields,
  methods/constructors/field constructors, properties/accessors, enums,
  constants, aliases, exceptions and lambdas, including nested declarations.
- [ ] Parser: generic/nullable/annotated types and every initializer/reference
  form in the checked-in grammar.
- [ ] Malformed-input regression cases with precise source diagnostics.
- [x] Parse every baseline repository `.lime` file with measured coverage and
  no silent skips; record and explain any deliberate syntax differences.

## M2: model and semantics

- [x] Deterministic recursive input collection, multiple inputs,
  deduplication, and auxiliary-source loading.
- [x] Global symbols, nested qualified names and forward references.
- [x] Import validation and Kotlin-equivalent ambiguity across imports and all
  enclosing scopes; include a no-nearest-scope-shadowing regression case.
- [ ] Duplicate declarations and signatures, while retaining legal overloads.
- [ ] Type references/target kinds and alias-cycle validation.
- [ ] Inheritance kinds/cycles and applicable open/narrow constraints.
- [ ] Parameter/field/enumerator duplicates, `Void` restrictions, throws
  targets, field-constructor references and obvious invalid defaults.
- [x] Document the exact validator set and remaining Kotlin validation gaps.
- [x] Successfully load the calculator and coherent real repository fixture
  groups with correct input/auxiliary boundaries.

## M3: CLI and JSON

- [ ] Help/version, input/auxinput/output, validation and syntax/model
  inspection, explicit generator selection and documented legacy flag aliases.
- [x] Correct nonzero failures for bad inputs/options/unsupported generators;
  no output writes during validation.
- [ ] Versioned, deterministic JSON containing parsed metadata and resolved
  references, usable for the calculator and broad LIME feature inspection.
- [ ] CLI integration checks, including paths with spaces and multi-file input.

## M4: C++17 backend

- [x] Define and document supported C++ API/naming/type mappings and limitations.
- [ ] Classes/interfaces, virtual methods/factories, properties, structs,
  enums, aliases and lambdas within that contract.
- [ ] Primitive/string/blob/container/optional/reference mappings and supported
  constants/defaults.
- [ ] Nested and cross-file dependencies, forwards/definition order and cycle
  diagnostics.
- [ ] Auxiliary declarations are resolved but not emitted.
- [ ] Explicit diagnostics for unsupported code-affecting attributes,
  descriptors, throwing behavior, runtime types or initializers.
- [ ] Render all selected outputs before writing; detect path/name collisions
  and verify generation failures do not leave partial generated artifacts.
- [ ] Compile generated declarations and run a C++17 consumer across multiple
  inputs; include supported existing repository input in acceptance evidence.

## M5: verification and handoff

- [x] `cargo fmt --check`.
- [x] `cargo clippy --all-targets -- -D warnings`.
- [ ] `cargo test`, including lexer/parser, semantic, corpus, CLI and C++ cases.
- [ ] Targeted JVM differential validation checks, including success, missing
  references, ambiguous scope/import lookup, and cycles where applicable.
- [ ] Determinism and failure-output behavior checked.
- [x] Write `README.md` with build/run examples, architecture, measured
  coverage, compatibility table, supported semantics and exact limitations.
- [ ] Independent Sol 6.1 xhigh review; fix and recheck material findings.
- [ ] Update this checklist with evidence and deferred items; create logical
  local commits, leaving the repository clean.

## Deferred full-parity work

- [ ] Complete every upstream semantic validator, filters/tags, documentation
  parser and warning/strict modes.
- [ ] Exact C++ output/runtime/name rules and existing C++ functional parity.
- [ ] Java/Kotlin plus JNI and Android runtime parity.
- [ ] Swift plus CBridge and Apple runtime parity.
- [ ] Dart plus FFI and Dart runtime parity.
- [ ] Options files/all flags, output caching, split outputs and build-system
  integration parity.
- [ ] Existing-platform smoke/functional parity, distribution, performance
  measurements and migration/cutover policy.

## Evidence log

- Planning baseline: `2044ae5c73e8b9521fac6dec6cd6133086dd4136`.
- Source inventory at planning: 251 production Kotlin files, 315 templates,
  345 `.lime` inputs / 18,471 lines. Corpus scenarios must be loaded separately
  for semantic checks because names repeat across fixtures.
- The existing installed JVM distribution can serve as a differential oracle;
  the Rust compiler must function independently of it.

- Native preview implementation: frontend, resolver, CLI, JSON and limited C++ backend; see README for specific incomplete behavior. Twelve integration tests cover 345/345 individually tracked inputs, calculator, four coherent smoke groups and two compiled C++ fixture groups.
- Rust checks passed: `cargo fmt --check`, `cargo clippy --offline --all-targets -- -D warnings`, `cargo test --offline` (12 integration tests). Template inventory tests: `python3 -m unittest discover -s tools/tests` (2 tests).
- Independent JVM smoke comparison: Rust validates 46 of 49 groups; three need platform filtering (`defaults_const`, `name_clash_overloads`, `skip`). `comments` requires JVM documentation configuration. The JVM accepts some invalid Void positions and duplicate parameters that this preview rejects.
- Preview remains incomplete: full grammar rejection, complete semantic checks, C++ nested/auxiliary references, feature guards and output parity remain open above. Independent review has not yet occurred.
