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
- [x] Malformed-input regression cases with precise source diagnostics.
- [x] Parse every baseline repository `.lime` file with measured coverage and
  no silent skips; record and explain any deliberate syntax differences.

## M2: model and semantics

- [x] Deterministic recursive input collection, multiple inputs,
  deduplication, and auxiliary-source loading.
- [x] Global symbols, nested qualified names and forward references.
- [x] Import validation and Kotlin-equivalent ambiguity across imports and all
  enclosing scopes; include a no-nearest-scope-shadowing regression case.
- [x] Duplicate declarations and signatures, while retaining legal overloads.
- [x] Type references/target kinds and alias-cycle validation.
- [x] Inheritance kinds/cycles and applicable open/narrow constraints.
- [ ] Parameter/field/enumerator duplicates, `Void` restrictions, throws
  targets, field-constructor references and obvious invalid defaults.
- [x] Document the exact validator set and remaining Kotlin validation gaps.
- [x] Successfully load the calculator and coherent real repository fixture
  groups with correct input/auxiliary boundaries.

## M3: CLI and JSON

- [x] Help/version, input/auxinput/output, validation and syntax/model
  inspection, explicit generator selection and documented legacy flag aliases.
- [x] Correct nonzero failures for bad inputs/options/unsupported generators;
  no output writes during validation.
- [x] Versioned, deterministic JSON containing parsed metadata and resolved
  references, usable for the calculator and broad LIME feature inspection.
- [ ] CLI integration checks, including paths with spaces and multi-file input.

## M4: C++17 backend

- [x] Define and document supported C++ API/naming/type mappings and limitations.
- [x] Classes/interfaces, virtual methods/factories, properties, structs,
  enums, aliases and lambdas within that contract.
- [ ] Primitive/string/blob/container/optional/reference mappings and supported
  constants/defaults.
- [ ] Nested and cross-file dependencies, forwards/definition order and cycle
  diagnostics.
- [ ] Auxiliary declarations are resolved but not emitted.
- [x] Explicit diagnostics for unsupported code-affecting attributes,
  descriptors, throwing behavior, runtime types or initializers.
- [ ] Render all selected outputs before writing; detect path/name collisions
  and verify generation failures do not leave partial generated artifacts.
- [x] Compile generated declarations and run a C++17 consumer across multiple
  inputs; include supported existing repository input in acceptance evidence.

## M5: verification and handoff

- [x] `cargo fmt --check`.
- [x] `cargo clippy --all-targets -- -D warnings`.
- [x] `cargo test`, including lexer/parser, semantic, corpus, CLI and C++ cases.
- [x] Targeted JVM differential validation checks, including success, missing
  references, ambiguous scope/import lookup, and cycles where applicable.
- [x] Determinism and failure-output behavior checked.
- [x] Write `README.md` with build/run examples, architecture, measured
  coverage, compatibility table, supported semantics and exact limitations.
- [x] Independent Sol 6.1 xhigh review; fix and recheck material findings.
- [x] Update this checklist with evidence and deferred items; create logical
  local commits, leaving the repository clean.

## M6: template and reference-model migration evidence

- [x] Inventory template helpers and model access sites with a reproducible static tool; see [TEMPLATE_SURFACE.md](TEMPLATE_SURFACE.md).
- [x] Implement a bounded experimental JVM reference-model snapshot tool with documented schema and tests; see [reference-model](tools/reference-model/README.md).
- [x] Add a reproducible JVM/Rust validation comparison runner covering core cases and coherent smoke groups.
- [ ] Build the canonical Kotlin model adapter, Rust JSON importer, template runtime and golden-output parity. The reference snapshot and Rust preview JSON are distinct schemas.
- [ ] Keep the existing Mustache templates unchanged and execute the custom Rust compatibility runtime stage below against Trimou helper, reflection, lookup, partial, and whitespace fixtures, followed by byte-exact output comparisons.

## M7 / P1a: executable template and graph-import slice

These are implementation tasks for the continuation, not evidence of delivered
behavior. The complete canonical adapter and C++ backend remain open.

- [x] Inspect actual Trimou configuration, custom helper semantics, candidate
  C++ templates and existing snapshot schema; choose the bounded custom-runtime
  stage in [PLAN.md](PLAN.md#p1a-executable-mustache-and-snapshot-compatibility-slice--next-increment).
- [x] Commit this continuation plan/checklist before runtime/oracle changes.
- [ ] Implement a source-aware parser for the existing Trimou dialect; parse
  all 315 unchanged production templates, preserving inline partials, comments,
  arguments and section structure. Verify the production corpus hash is unchanged.
- [ ] Import version-1 reference snapshots with validated IDs, references,
  sharing/cycles, enum and value shapes; reject malformed/unsupported documents.
- [ ] Define and document explicit property views, scoped render context,
  helper registrations and captured oracle name/predicate tables where used.
- [ ] Implement the shared `gluecodium.template.render-request` version-1
  protocol (`template`, `data`, optional `snapshot`, `property_overlays`,
  `hooks`) and `render --templates DIR --request FILE [--output FILE]` CLI;
  distinguish replayed C++ hook results from native resolver implementation.
- [ ] Execute context lookup, sections and iteration metadata; `if`/`unless`,
  scoped `set`, partials/inline partials, `prefix`/`prefixPartial`,
  `join`/`joinPartial`, instance tests, and the selected `resolveName`/predicate
  contracts. Reject unimplemented executed helpers/selectors explicitly.
- [ ] Add native library/CLI graph inspection and named-template rendering;
  render before writing and preserve existing outputs on failures.
- [ ] Add an actual-JVM-Trimou oracle and reproducible fixtures/configuration,
  including exact UTF-8 expected bytes and distribution/template provenance.
- [ ] Compare helper scope, missing/null values, section context, `iter`,
  standalone whitespace, partial indentation, multiline prefix trimming and
  final newlines directly against the configured JVM engine.
- [ ] Compare unchanged `cpp/CppEnumeration`, `cpp/CppTypeAlias`,
  `cpp/CppFunctionSignature`, `cpp/CppReturnType` and transitive partials on a
  documented nontrivial model/configuration matrix; include configured
  `cpp/common/Export`. Record case-level limitations without a whole-C++ claim.
- [ ] Run `cargo fmt --check`, offline Clippy with warnings denied, Cargo tests,
  existing Python tooling checks and the new oracle reproducibility/differential
  checks; retain the preview corpus and C++ consumer coverage.
- [ ] Obtain independent Sol 6.1 xhigh review; fix material findings and record
  exact evidence and remaining helper/view/naming/canonical-boundary gaps.
- [ ] Update README/review/evidence/checklist to the delivered scope, commit
  logical increments and push the authorized branch after verification.

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

- Native preview implementation: frontend, resolver, CLI, JSON and limited C++ backend; see README for specific incomplete behavior. Twenty-two integration tests cover 345/345 individually tracked upstream baseline inputs (excluding the port’s own negative `.lime` fixtures; 348 LIME files are now tracked in the full repository), calculator, four coherent smoke groups and two compiled C++ fixture groups.
- Rust checks passed: `cargo fmt --check`, `cargo clippy --offline --all-targets -- -D warnings`, `cargo test --offline` (22 integration tests). Python tool tests: `python3 -m unittest discover -s tools/tests` (4 tests). An optimized `cargo build --release` also passed; the release CLI exported calculator JSON and generated C++ from the multi-input repository fixture.
- Independent JVM smoke comparison: Rust validates 46 of 49 groups; three need platform filtering (`defaults_const`, `name_clash_overloads`, `skip`). `comments` requires JVM documentation configuration. The JVM accepts some invalid Void positions and duplicate parameters that this preview rejects.
- Preview remains incomplete: full grammar rejection, complete semantic checks, C++ nested/auxiliary references, feature guards and output parity remain open above. Independent Sol 6.1 xhigh review and recheck are recorded in [REVIEW.md](REVIEW.md); material findings were fixed with regression coverage. The final bounded review covered 47 focused cases, compiled all 10 generated-success headers with strict C++17 flags, and ran ordered-container consumers.

- The optimized release validation comparison has 58 cases and no unexpected acceptance differences; four smoke differences are explicitly recorded, and the JVM crashes with stack overflow on two cycle cases. This is acceptance evidence only.
- Remaining preview gaps include structured diagnostic objects, complete syntax rejection and dotted quoted identifiers, full metadata fidelity, runtime-dependent C++ behavior, nested and auxiliary C++ type references, constants/defaults, platform filtering, and full upstream validator parity. C++ guards reject these unsupported cases where implemented.
- Continuation baseline: `6bb3214a2`. The next stage selects a custom Rust
  Trimou-compatible parser/runtime, a validated version-1 reference-graph
  importer, explicit bounded property/helper views and an actual JVM byte
  oracle. It preserves all 315 production Mustache templates and keeps
  whole-C++, complete canonical-model and native naming parity unclaimed.
- Continuation roles retain Sol 6.1 max planning and Sol 6.1 xhigh review;
  the user's subsequent instruction selects Terra 6.1 xhigh for the next
  implementation work.
