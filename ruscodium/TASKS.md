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
- [ ] Build the complete canonical Kotlin model adapter and establish full template and generated-output parity. The experimental reference snapshot and Rust preview JSON are distinct schemas.
- [x] Keep the existing Mustache templates unchanged and execute the bounded Rust compatibility runtime against selected Trimou helper, model-view, lookup, partial and whitespace fixtures with byte-exact comparisons.

## M7 / P1a: executable template and graph-import slice

This bounded slice is implemented as described in [TEMPLATES.md](TEMPLATES.md).
The complete canonical adapter and C++ backend remain open.

- [x] Inspect actual Trimou configuration, custom helper semantics, candidate
  C++ templates and existing snapshot schema; choose the bounded custom-runtime
  stage in [PLAN.md](PLAN.md#p1a-executable-mustache-and-snapshot-compatibility-slice--bounded-milestone-delivered).
- [x] Commit this continuation plan/checklist before runtime/oracle changes.
- [x] Parse all 315 unchanged production templates, preserving inline partials,
  comments, arguments and section structure. Verify the production corpus hash.
- [ ] Complete source-position diagnostics and full Trimou syntax validation.
- [x] Import version-1 reference snapshots with validated IDs and references,
  preserving sharing and cycles and rejecting malformed graph references.
- [x] Define and document explicit property views, scoped render context,
  helper registrations and captured oracle name/predicate tables where used.
- [x] Implement the shared `gluecodium.template.render-request` version-1
  protocol (`template`, `data`, optional `snapshot`, `property_overlays`,
  `absent_properties`, `hooks`) and `render --templates DIR --request FILE [--output FILE]` CLI;
  distinguish replayed C++ hook results from native resolver implementation.
- [x] Execute context lookup, sections and iteration metadata; `if`/`unless`,
  scoped `set`, partials/inline partials, `prefix`/`prefixPartial`,
  `join`/`joinPartial`, instance tests, and the selected `resolveName`/predicate
  contracts. Reject unimplemented executed helpers/selectors explicitly.
- [x] Expose native library graph inspection and named-template rendering via
  library and CLI; render before writing and preserve outputs on failures.
- [ ] Add a standalone CLI graph inspector.
- [x] Add an actual-JVM-Trimou oracle and reproducible fixtures/configuration,
  including exact UTF-8 expected bytes and distribution/template provenance.
- [x] Compare helper scope, missing/null values, section context, `iter`,
  standalone whitespace, partial indentation, multiline prefix trimming and
  final newlines directly against the configured JVM engine.
- [x] Compare unchanged `cpp/CppEnumeration`, `cpp/CppTypeAlias`,
  `cpp/CppFunctionSignature`, `cpp/CppReturnType` and transitive partials on a
  documented nontrivial model/configuration matrix; include configured
  `cpp/common/Export`. Record case-level limitations without a whole-C++ claim.
- [x] Run `cargo fmt --check`, offline Clippy with warnings denied, Cargo tests,
  existing Python tooling checks and the new oracle reproducibility/differential
  checks; retain the preview corpus and C++ consumer coverage.
- [x] Obtain independent Sol 6.1 xhigh review; fix material findings and record
  exact evidence and remaining helper/view/naming/canonical-boundary gaps.
- [x] Update README/review/evidence/checklist to the delivered scope, commit
  logical increments and push the authorized branch after verification.

## M8 / P1a.1: strict native C++ naming

This bounded increment follows
[PLAN.md](PLAN.md#m8--p1a1-strict-native-c-naming--bounded-implementation-delivered).
It keeps all 315 production templates unchanged and leaves predicates/sorters
at their measured replay boundary.

- [x] Inspect current renderer/graph/oracle contracts and Kotlin
  `CppNameResolver`, `CppFullNameResolver`, `CppNameCache`, `NameRules`,
  `NameHelper` and default C++ naming configuration.
- [x] Define explicit `native_cpp` opt-in, namespace options, supported native
  scope, strict rejection/failure behavior, ownership and acceptance evidence.
- [x] Commit this plan/checklist before implementation changes.
- [x] Add validated native config and separate resolver dispatch; retain legacy
  replay when omitted, reject nonempty `hooks.names` when enabled, and never
  fall back to captured name results.
- [x] Index real model declarations/parents and port default ASCII name rules,
  declaration names and FQN semantics, including namespace configuration.
  Reject incomplete traversable parent context instead of guessing.
- [x] Port required built-in, enum/alias, return/type-reference, nullable,
  class/interface, list/map/set and hash spellings; test alias-aware actual-type
  behavior and bounded cycle/missing-fact errors.
- [x] Port the measured ordinary literal/constant-reference matrix and
  property/field getter/setter rules, including boolean aliases and proven
  `@Cpp(Accessors)` parent context.
- [x] Honor and JVM-test supported `@Cpp(Name)`, accessor names, `@Cpp(Type)`
  and `@Optimized` behavior; reject unsupported naming attributes, externals,
  nonempty comments, complex defaults and custom naming files before writes.
- [x] Inventory all existing recorded name cells; compare every supported cell
  natively with recordings used only as expectations, and assert/report exact
  unsupported cases. Extend JVM-derived parent context where old snapshots
  cannot prove a supported result.
- [x] Add reproducible comment-free JVM cases rendering the four unchanged
  real C++ templates and partials with no name hooks, including function
  attributes; compare exact bytes and preserve the original replay fixtures.
- [x] Expand independent JVM name cells for namespace/type/container/alias/
  accessor/attribute cases beyond the existing recordings; retain provenance.
- [x] Verify mixed-mode/config/selector/missing-context/unsupported/cycle
  failures preserve existing outputs and emit no partial stdout.
- [x] Pass formatting, offline Clippy, Cargo and existing Python/reference-model
  checks, JVM oracle reproduction, unchanged-template checks and retained
  preview corpus/C++ consumer coverage.
- [x] Obtain independent Sol 6.1 xhigh review, fix material findings, and record
  the review and scope evidence.
- [x] Push the authorized branch after final verification.

The differential inventory currently accounts for 223 recorded calls: 203 exact
matches and 20 explicit rejections (14 missing parent contexts, four unavailable
or nonempty comments, and two unsupported `@Cpp(Attribute)` cases). The
full-model matrix contributes 162 exact matches. The native renderer also
matches JVM bytes for four unchanged, comment-free C++ partials without name
hooks. At implementation commit `12aac6c45`, formatting, offline Clippy,
49 Rust tests, four Python tests, the reference-model export checks, all 34 JVM
oracle cases and release build passed. These measurements do not establish
complete naming or backend parity. Published this verified increment through
`121ef5981` to `origin/ruscodium/rust-port`.

## M9 / P1a.2: strict native C++ predicates and declaration sorting

Execute [the M9 contract](PLAN.md#m9--p1a2-strict-native-c-predicates-and-declaration-sorting--bounded-implementation-delivered)
from baseline `96b7c3421`, with Sol 6.1 max planning, Terra 6.1 xhigh
implementation and independent Sol 6.1 xhigh review. Keep every change under
`ruscodium/` and all 315 upstream Mustache templates unchanged.

- [x] Read existing plan/runtime/oracle contracts and actual Kotlin predicates,
  helper collectors, immutable-field traversals and default topological sorter.
- [x] Define explicit native predicate/sorter options, exact algorithm scope,
  comment/getter boundary, anti-replay rules and completion evidence.
- [x] Commit this plan/checklist before M9 implementation starts.
- [x] Add validated `native_cpp.predicates` and `.sorters` boolean opt-ins,
  default false; retain M8/legacy dispatch and reject enabled-provider replay
  hooks/catalog, including configuration and empty-input selector guards.
- [x] Port all eleven C++ predicate selectors from raw model facts, preserving
  actual receiver-kind behavior, aliases, nullability, constructors/defaults,
  the two immutable-field traversals, sibling imports and ancestor skip rules.
- [x] Keep missing/nonempty comment content strict; honor empty-comment
  exclusion/deprecation and non-null warnings without captured predicate answers.
- [x] Port the actual default sorter: named-element filtering, exact dependency
  dispatch, generic children and direct alias identities, input-order ties,
  self-dependency removal, idempotence and explicit cycle/duplicate handling.
- [x] Add bounded graph projections needed by genuine `CppStruct`/`CppClass`
  partials; document each measured getter/ambient value. Native algorithms must
  not consume computed predicate answers, sorted lists or imported dependency
  collections. Prefer raw-derived views where the native logic already exists.
- [x] Inventory and compare every existing actual predicate cell and sorter
  record, with exact-match and explicit-rejection counts/reasons.
- [x] Extend reproducible full-model JVM predicate/sort matrices through the M9
  cases, including actual reordering, constructors/defaults, nested/alias and
  class refs, immutable containers, forward declarations and inherited skips.
- [x] Match JVM bytes for two or three unchanged comment-free C++ struct/class
  fragments with all hooks removed, native names/predicates/sorting enabled and
  at least one real declaration reordering; retain existing native fragments.
- [x] Verify raw-fact mutations change native results; cover hook/catalog
  anti-replay, empty lists, unknown selectors, missing facts, unsupported content
  and legal/invalid cycles with pre-write/stdout preservation checks.
- [x] Pass formatting, offline Clippy, Cargo, Python/reference-model checks,
  JVM fixture reproduction and 315-template equality; retain 49-test/34-case
  baseline coverage, preview corpus and compiled C++ consumers, recording counts.
- [x] Obtain independent Sol 6.1 xhigh review and fix material findings.
- [x] Update README, TEMPLATES, oracle, review and measured evidence/checklist;
  commit tested increments and push the authorized branch.

The current control inventory compares 1,095 actual predicate calls and 15
sort records exactly, with four explicit nonempty-comment rejections. Native
name comparison covers 295 exact calls and 20 documented rejections. Five
unchanged C++ partials match JVM bytes with all native providers enabled,
including fieldful defaults, immutable fields and an explicit field constructor;
the class case reorders a nested declaration. Actual JVM cases cover immutable
list, set, map-value and map-key fields with partial field constructors.

M9 does not complete canonical adaptation, raw/native comments, header/file-set
generation or C++ runtime/ABI parity. Keep those gaps explicit after delivery.

M9 was verified and published through `d2e69b620` on
`origin/ruscodium/rust-port`, including the independent review in `8667cbf1e`.
Final checks passed formatting, offline Clippy, 66 Rust tests, four Python tests,
reference-model checks, 41 JVM oracle cases, 315 unchanged templates and release
build. See [REVIEW.md](REVIEW.md) for the review artifact and exact disposition.

## M10 / P1b.1: native C++ whole-file generation from snapshots

Execute [the M10 contract](PLAN.md#m10--p1b1-native-c-whole-file-generation-from-snapshots--planned)
from `d2e69b620`, with Sol 6.1 max planning, Terra 6.1 xhigh implementation and
independent Sol 6.1 xhigh review. Keep changes under `ruscodium/`, production
Mustache unchanged, and the preview C++ generator separate.

- [x] Inspect actual C++ generator, include/forward collectors, output name
  rules, helper inventory, copyright resolver and existing native/view boundary.
- [x] Define the guarded full-file contract, strict versioned job, native
  collector/path ownership, frozen-getter allowlist policy and exact evidence.
- [x] Commit this plan/checklist before M10 implementation starts.
- [ ] Add the library generator and `generate-cpp --job FILE --templates DIR
  --output DIR`, validating schema/options and full `LimeModel` graph; forbid
  render contexts, output inventories, helper hooks and replay fallbacks.
- [ ] Define/test/document class-specific allowed measured getters/absences;
  reject generated includes/forwards/order/names/predicate controls and unknown
  overlays. Keep all native algorithms on raw model/reference facts.
- [ ] Implement fail-fast model/attribute/dependency guards for the documented
  comment-free class/interface, struct, enum, alias and lambda subset, including
  unsupported inheritance/docs/external/errors/equality/async/filtering cases.
- [ ] Derive generation roots and nested/reference/auxiliary ownership from the
  full graph; port output filename/path and namespace/export rules, including
  supported root renaming, defaults and distinct common exports.
- [ ] Port raw type/value walks, include resolution, header and implementation
  include collectors, self-includes, exact dedup/sort and forward groups, with
  generic, alias, nullable, class-reference and nested-type cases.
- [ ] Build actual header/implementation contexts internally and render unchanged
  `CppHeader`/`CppImplementation` plus transitive partials; generate the upstream
  .h/.cpp selection, including struct constructors and class destruction.
- [ ] Render all thirteen common headers, three common implementations and two
  exports with correct paths, source sets, macro/configuration data and copyright
  bytes. No unneeded helper may be silently omitted from full-file comparisons.
- [ ] Render/validate every output in memory before writes, detect model/helper
  path collisions/escapes and preserve existing output on input/render failures;
  verify determinism and leave unrelated files alone.
- [ ] Add a JVM oracle invoking actual `CppGenerator.generate` over independently
  loaded LIME, exporting snapshots/views separately from exact expected files;
  record compiler/template/input/options/source-set provenance and reproduction.
- [ ] Compare complete relative paths, source sets and every output byte for
  default and configured jobs; cover all root kinds, nested reorder, auxiliary
  references, forwards/nested includes, generic/nullable values and constructors.
- [ ] Prove raw type/path/name/declaration mutations affect includes, forwards,
  output paths/order/bytes without imported computed generator controls. Cover
  invalid jobs, context/replay injection, missing facts, unsupported content and
  collisions with no partial generated artifacts.
- [ ] Compile generated model/common implementations with strict C++17 flags and
  run a consumer using generated value types and an implemented interface.
- [ ] Pass formatting, offline Clippy/Cargo, Python/reference-model checks,
  whole-file oracle reproduction, retained 41 JVM template cases and 315-template
  equality, preview corpus and existing compiled consumers; record exact counts.
- [ ] Obtain independent Sol 6.1 xhigh review and fix material findings.
- [ ] Update README, TEMPLATES, oracle, review and measured checklist evidence,
  commit tested increments and push the authorized branch.

Completion requires actual full C++ generator file sets for the supported
snapshot subset, including eighteen common/export files per job. Canonical
adaptation, native comments, unsupported C++ features/runtime ABI and all
Dart/Swift/JNI/platform outputs remain deferred.

## Deferred full-parity work

- [ ] Complete every upstream semantic validator, filters/tags, documentation
  parser and warning/strict modes.
- [ ] Exact C++ output/runtime/name rules and existing C++ functional parity.
- [ ] Complete native C++ resolver/name-rule coverage beyond M8 and port
  predicates/sorters; legacy template requests still replay captured results.
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

- Native preview implementation: frontend, resolver, CLI, JSON and limited C++ backend; see README for specific incomplete behavior. Twenty-two integration tests cover 345/345 individually tracked upstream baseline inputs (excluding the port’s own `.lime` fixtures), calculator, four coherent smoke groups and two compiled C++ fixture groups.
- Rust checks passed: `cargo fmt --check`, `cargo clippy --offline --all-targets -- -D warnings`, `cargo test --offline` (22 integration tests). Python tool tests: `python3 -m unittest discover -s tools/tests` (4 tests). An optimized `cargo build --release` also passed; the release CLI exported calculator JSON and generated C++ from the multi-input repository fixture.
- Independent JVM smoke comparison: Rust validates 46 of 49 groups; three need platform filtering (`defaults_const`, `name_clash_overloads`, `skip`). `comments` requires JVM documentation configuration. The JVM accepts some invalid Void positions and duplicate parameters that this preview rejects.
- Preview remains incomplete: full grammar rejection, complete semantic checks, C++ nested/auxiliary references, feature guards and output parity remain open above. Independent Sol 6.1 xhigh review and recheck are recorded in [REVIEW.md](REVIEW.md); material findings were fixed with regression coverage. The final bounded review covered 47 focused cases, compiled all 10 generated-success headers with strict C++17 flags, and ran ordered-container consumers.

- The optimized release validation comparison has 58 cases and no unexpected acceptance differences; four smoke differences are explicitly recorded, and the JVM crashes with stack overflow on two cycle cases. This is acceptance evidence only.
- Remaining preview gaps include structured diagnostic objects, complete syntax rejection and dotted quoted identifiers, full metadata fidelity, runtime-dependent C++ behavior, nested and auxiliary C++ type references, constants/defaults, platform filtering, and full upstream validator parity. C++ guards reject these unsupported cases where implemented.
- Continuation baseline: `6bb3214a2`. The delivered bounded custom Rust
  Mustache runtime imports version-1 reference graphs and uses explicit property
  views and replayed helper results. The 315 production templates are unchanged;
  whole-C++, complete canonical-model and native naming parity remain open.
- The runtime's 19 integration tests include CLI byte comparisons against all
  29 JVM fixtures, graph and replay validation, path and recursion guards,
  failure-output preservation and parsing all 315 templates. The JVM oracle
  includes 15 review regressions for rejected inputs, plus its nested-comment
  negative check. The existing 22 preview tests retain their
  345-input corpus and compiled C++ consumer coverage.
- Final checks passed: formatting, offline Clippy with warnings denied, all 41
  Rust tests, four Python tooling tests, the reference-model tests, the JVM
  oracle with 29 byte fixtures and 315 template comparisons, and a release
  build. Independent Sol 6.1 xhigh review and 42 retained CLI probes are
  recorded in [REVIEW.md](REVIEW.md); no material findings remain within this
  bounded stage.
- Continuation roles retain Sol 6.1 max planning and Sol 6.1 xhigh review;
  the user's subsequent instruction selects Terra 6.1 xhigh for the next
  implementation work.
- Published the verified continuation through `4f5dd0f8e` to
  `origin/ruscodium/rust-port`; the remaining unchecked items describe later
  compatibility work.
