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
- [ ] Define the template-complete canonical model contract, implement the native Rust frontend adapter with full Kotlin-model semantic parity, and establish full template/generated-output parity. The experimental reference snapshot and Rust preview JSON are distinct schemas; M12's bounded adapter to the existing compatibility backend is tracked separately and does not complete this item.
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

Execute [the M10 contract](PLAN.md#m10--p1b1-native-c-whole-file-generation-from-snapshots--guarded-subset-delivered)
from `d2e69b620`, with Sol 6.1 max planning, Terra 6.1 xhigh implementation and
independent Sol 6.1 xhigh review. Keep changes under `ruscodium/`, production
Mustache unchanged, and the preview C++ generator separate.

- [x] Inspect actual C++ generator, include/forward collectors, output name
  rules, helper inventory, copyright resolver and existing native/view boundary.
- [x] Define the guarded full-file contract, strict versioned job, native
  collector/path ownership, frozen-getter allowlist policy and exact evidence.
- [x] Commit this plan/checklist before M10 implementation starts.
- [x] Add the library generator and `generate-cpp --job FILE --templates DIR
  --output DIR`, validating schema/options and full `LimeModel` graph; forbid
  render contexts, output inventories, helper hooks and replay fallbacks.
- [x] Define/test/document class-specific allowed measured getters/absences;
  reject generated includes/forwards/order/names/predicate controls and unknown
  overlays. Keep all native algorithms on raw model/reference facts.
- [x] Implement fail-fast model/attribute/dependency guards for the documented
  comment-free class/interface, struct, enum, alias and lambda subset, including
  unsupported inheritance/docs/external/errors/equality/async/filtering cases.
- [x] Derive generation roots and nested/reference/auxiliary ownership from the
  full graph; port output filename/path and namespace/export rules, including
  supported root renaming, defaults and distinct common exports.
- [x] Port raw type/value walks, include resolution, header and implementation
  include collectors, self-includes, exact dedup/sort and forward groups, with
  generic, alias, nullable, class-reference and nested-type cases.
- [x] Build actual header/implementation contexts internally and render unchanged
  `CppHeader`/`CppImplementation` plus transitive partials; generate the upstream
  .h/.cpp selection, including struct constructors and class destruction.
- [x] Render all thirteen common headers, three common implementations and two
  exports with correct paths, source sets, macro/configuration data and copyright
  bytes. No unneeded helper may be silently omitted from full-file comparisons.
- [x] Render/validate every output in memory before writes, detect model/helper
  path collisions/escapes and preserve existing output on input/render failures;
  verify determinism and leave unrelated files alone.
- [x] Add a JVM oracle invoking actual `CppGenerator.generate` over independently
  loaded LIME, exporting snapshots/views separately from exact expected files;
  record compiler/template/input/options/source-set provenance and reproduction.
- [x] Compare complete relative paths, source sets and every output byte for
  default and configured jobs; cover all root kinds, nested reorder, auxiliary
  references, forwards/nested includes, generic/nullable values and constructors.
- [x] Prove raw type/path/name/declaration mutations affect includes, forwards,
  output paths/order/bytes without imported computed generator controls. Cover
  invalid jobs, context/replay injection, missing facts, unsupported content and
  collisions with no partial generated artifacts.
- [x] Compile generated model/common implementations with strict C++17 flags and
  run a consumer using generated value types and an implemented interface.
- [x] Pass formatting, offline Clippy/Cargo, Python/reference-model checks,
  whole-file oracle reproduction, retained 41 JVM template cases and 315-template
  equality, preview corpus and existing compiled consumers; record exact counts.
- [x] Obtain independent Sol 6.1 xhigh review and fix material findings.
- [x] Update README, TEMPLATES, oracle, review and measured checklist evidence,
  commit tested increments and push the authorized branch.

Current evidence: 77 Rust tests passed with offline Clippy; the two whole-file
fixtures compare 50 file paths, source sets and byte contents, including 18
common/export files per job. Native-generated C++ and the JVM captures both
compiled and ran their consumers with `-std=c++17 -Wall -Wextra -Werror`. The
default fixture covers a set and nested aliases in dependency-reversed order.
Raw type, C++ name, package path and declaration-order mutations are tested
without changing getter overlays. Independent Sol 6.1 xhigh review passed at
`6b1de0233` and is recorded in `18bea9403`; no material finding remains open
within the guarded scope. Final formatting, offline all-target Clippy, the 77
Rust tests (including the 345-input preview corpus and compiled consumers),
four Python tests, reference-model checks, both fresh JVM oracles, all 315
unchanged templates and the release build passed. M10 implementation, review,
plan and verification were pushed through `ab1f9a5b1` to
`origin/ruscodium/rust-port`; this checklist records that confirmed publication.

Completion requires actual full C++ generator file sets for the supported
snapshot subset, including eighteen common/export files per job. Canonical
adaptation, native comments, unsupported C++ features/runtime ABI and all
Dart/Swift/JNI/platform outputs remain deferred.

## M11 / P1b.2: smoke acceptance inventory and bounded native documentation

Execute [the M11 contract](PLAN.md#m11--p1b2-smoke-acceptance-inventory-and-bounded-native-documentation--guarded-subset-delivered)
from clean `d9dc5b901`, with Sol 6.1 max planning, Terra 6.1 xhigh implementation
and independent Sol 6.1 xhigh review. Keep every change under `ruscodium/` and
all 315 production templates unchanged. M10 evidence above remains historical.

- [x] Inspect the snapshot/private-comment boundary, native names/controls,
  unchanged C++ documentation partials, upstream comment processing and actual
  smoke inputs/options; define bounded scope and exact acceptance first.
- [x] Commit this M11 plan/checklist before new implementation starts.
- [x] First add a reproducible acceptance runner/report for the thirteen named
  complete smoke groups; pin baseline outcomes, exact input/auxiliary hashes,
  placeholders/options/tags, compiler/template provenance and native revision.
- [x] Export the original unfiltered loader model and invoke the real JVM C++
  generator independently with effective smoke options. Distinguish native
  rejection, output mismatch, JVM failure and exporter failure; retain all rows.
- [x] For admitted cases compare every path, source set and byte, including all
  common/export files; report baseline-to-final counts and concrete blockers
  without counting guarded rejections as compatibility successes.
- [x] Add version-2 generation jobs with complete ordered `raw_comments` pairs
  per `LimeComment`; keep snapshot v1 and existing default/custom v1 fixtures
  unchanged, reject the new field in v1 and forbid v2 measured-empty fallback.
- [x] Add opt-in, narrowly checked oracle reflection for raw tagged sections;
  record its schema/provenance without changing production Kotlin or default
  reference export. Reject selected/formatted comment projections and v2
  comment `isEmpty` overlays.
- [x] Implement native raw emptiness, exact Cpp/universal section selection,
  ordered placeholder expansion and source trimming/blankness; validate complete
  maps, pair/value/target shapes, keys and IDs with cycle/depth/size bounds.
- [x] Measure and implement a documented plain Unicode/paragraph/newline
  formatting subset; guard Markdown and documentation links after expansion,
  with actual JVM positive and rejected-syntax evidence.
- [x] Integrate native comment names, template `isEmpty`, `hasAnyComment`, raw
  exclusion, function/property/field/constructor docs, and path-derived lambda
  `parameterName`; preserve legacy requests and unrelated feature guards.
- [x] Match complete JVM outputs for the separately loaded, unmodified
  `CommentsInterface.lime` and `CommentsLambda.lime` upstream files; keep the
  complete comments-group outcome separate from these focused successes.
- [x] Add focused real-LIME whole-file evidence for Unicode, paragraphs,
  platform-only/mixed text, ordering, placeholders, exclusion, parameters,
  returns, properties and struct/field-constructor documentation.
- [x] Prove raw mutations change comments/presence/platform/placeholder output
  without recorded results; cover raw-empty versus selected-empty/blank text,
  other-platform-only text and empty placeholder expansions.
- [x] Reject incomplete/malformed/cyclic documentation, forged answers and
  unsupported expanded Markdown/links, including auxiliary and late cases,
  before writes; preserve stdout/output sentinels and deterministic repetition.
- [x] Compile all new generated implementations with strict C++17 flags and run
  a meaningful consumer; reproduce native output with the JVM unavailable.
- [x] Pass formatting, offline all-target Clippy/Cargo, Python/reference-model
  checks, retained whole-file/template oracles, all 315 unchanged templates,
  preview corpus and compiled consumers, plus new smoke/documentation evidence.
- [x] Obtain independent Sol 6.1 xhigh review and fix material findings.
- [x] Finalize measured docs/evidence with exact counts and commit/push tested
  increments.

Full Markdown/link processing, native structured-documentation/LIME frontend
adaptation, filtering, inheritance, externals, new attributes and broader C++
runtime/ABI compatibility remain deferred. The smoke inventory determines the
impact ordering for later feature increments; M11 does not relax those guards.

Measured evidence: native implementation `84377ae1e` and oracle/inventory
tooling through `1dedc2ac8` pass 87 Rust tests, formatting, offline all-target
Clippy, four Python tests, reference-model checks, the 41 retained JVM
template cases and all 315 unchanged templates. Both existing whole-file
jobs retain their 50 exact files; three new documentation jobs add 63 exact
files, with native/JVM paths, source sets and every byte compared. All five
native-generated consumers and corresponding JVM consumers compiled and ran
with strict C++17 warnings. Native runs with empty `PATH` were deterministic.

The reproduced smoke reports retain 1 exact complete group and 12 guarded
rejections among 13. Both separately loaded upstream documentation files
move from rejection to exact match; the complete comments group remains
rejected. No matrix row has an output mismatch or JVM/export failure.
First rejection diagnostics identify observed blockers, not every feature
in a rejected model. See [the inventory](tools/cpp-smoke-matrix/README.md).

Independent Sol 6.1 xhigh review, recorded in `2696d4be8`, found no unresolved
material finding in the guarded scope. Its formatter differential admitted 1,643 of 7,203
cases with no JVM byte mismatch; other forms remain guarded. Thirty-seven
negative CLI probes kept stdout empty and preserved existing files. Synthetic empty
placeholder DAG/depth checks exercise bounded expansion independently of
the one-level real-loader fixture. See [REVIEW.md](REVIEW.md) for exact
candidate hashes and findings. Implementation, oracle/report, independent
review, plan and verification were pushed through `47e86a969` to
`origin/ruscodium/rust-port`; this checklist records the confirmed publication.

## M12 / P1c: native frontend adapter to the C++ compatibility backend

Execute [the M12 contract](PLAN.md#m12--p1c-native-frontend-adapter-to-the-c-compatibility-backend--bounded-subset-delivered)
from clean `d1966f390` on `ruscodium/rust-port`, with Sol 6.1 max planning,
Terra 6.1 xhigh implementation and independent Sol 6.1 xhigh review. Keep all
changes under `ruscodium/`, all 315 production templates unchanged, and the
preview generator/API separate. M6's full canonical parity item remains open.

- [x] Inspect the native model/parser/resolver, strict backend graph/getter
  contract and independently captured default/custom inputs/options/outputs.
- [x] Define the bounded native adapter, no-JVM compile path, source-fact guards,
  separate CLI/options contract and exact acceptance gates in PLAN/TASKS.
- [x] Commit this M12 plan/checklist before implementation starts.
- [x] Retain type-position docs in `TypeRef.docs`, omitting empty values from
  preview JSON; account for every consumed metadata position before adaptation.
- [x] Add public `cpp_adapter` adaptation/generation APIs accepting native
  `Model` plus options; clone, recursively clear resolved caches and re-resolve/
  validate caller-constructed models, never trust stale targets or accept backend
  graph/view/context/replay injection.
- [x] Define explicit AST kind/field/attribute/literal guards for the admitted
  surface, including schema/names/imports, builtin consistency, raw/structured
  value agreement, auxiliary/late declarations and recursive type metadata;
  reject unsupported facts before constructing empty replacements, with no
  fixture-name/path/input allowlist.
- [x] Build deterministic complete typed backend graphs with all seventeen
  builtins, main/auxiliary roots, reference/file-name maps, paths/owners,
  attributes/comments, ordered members, type refs/containers/aliases,
  methods/returns/parameters/accessors, defaults/enumerators/field constructors.
- [x] Derive getter views, child-type collections, implicit accessor/return
  semantics and checked missing properties from native facts; keep strict
  backend shape/reference/ownership validation enabled with no generic fallback.
- [x] Produce v2 jobs with complete raw comment arrays, deriving emptiness only
  after guarding all retained source docs, including type-local/auxiliary docs;
  do not reuse legacy measured comment-emptiness answers.
- [x] Add `compile-cpp` with repeated `--input`/`--auxinput`, required
  `--templates`/`--output` and optional `--options`; reject unknown, duplicate
  scalar and missing options while preserving the existing preview commands.
- [x] Add strict `gluecodium.native-cpp-options` v1 configuration for
  root/internal namespaces, export/common-export and nullable copyright text,
  with existing defaults, identifier checks and no generated model controls.
- [x] Reuse `cpp_generation::generate` and `write_files`; render every output
  before writes and preserve stdout/output sentinels on all pre-write failures.
- [x] Compare native-LIME default/custom output to all 26/24 existing actual
  JVM-captured paths, source sets and bytes, including eighteen common/export
  files per job; assert auxiliary ownership and exact fifty-file totals.
- [x] Compare a documented semantic graph projection with independently loaded
  JVM models, normalizing IDs/source roots while preserving meaningful order,
  kinds/owners/types/attributes/accessors/defaults/constructor links/comments;
  enumerate field coverage and exclusions without a full canonical claim.
- [x] Compile all native-generated model/common implementations and run both
  existing consumers with strict C++17 warnings; cover library and CLI paths.
- [x] Run native LIME compilation from a temporary working directory with empty
  `PATH`, no JVM/captured job dependency and deterministic repetition.
- [x] Differentially test native source mutations for names/paths/order,
  generic/nullable/class refs, values and auxiliary lookup/ownership against
  independently generated JVM files for admitted cases.
- [x] Test malformed/forged mutable models, stale refs, invalid config,
  unsupported source/metadata, collisions and render failures, including
  auxiliary/late cases, with no partial output and retained sentinels.
- [x] After the fifty-file gate, map feasible bounded source documentation to
  M11's raw v2 contract with real-LIME/JVM whole-file evidence; preserve facts,
  reject unsupported forms and report exact admission/deferment blockers.
- [x] Retain all 63 existing documentation files as backend regressions; label
  which real-LIME units the native adapter admits without gating on full
  Markdown/link or complete comments-group parity.
- [x] Pass formatting, offline all-target Clippy/Cargo, Python/reference-model
  checks, retained whole-file/documentation/template oracles, preview corpus
  and compiled consumers, and equality of all 315 production templates.
- [x] Obtain independent Sol 6.1 xhigh review and fix material findings.
- [x] Finalize README, generation/model/oracle/review documentation and measured
  checklist evidence with exact counts/limits, then commit/push tested increments.

The mandatory first acceptance gate is the native LIME pipeline's fifty exact
default/custom files plus semantic, no-JVM, failure and compiled-consumer
evidence. Bounded documentation follows and is reported separately; unsupported
source facts must be diagnosed. Full canonical/Kotlin-model parity, complete
documentation/validation and broader C++ runtime/platform work remain deferred.

Delivered evidence: native adapter and source corrections through
`b73b483be`, verification tools through `0d2fa01fb`, and usage documentation
in `4c91e507a` complete the bounded native path. The four real-LIME baseline
jobs compare 90 paths, source sets and exact file bytes: default 26, custom
24, upstream interface documentation 20 and upstream lambda documentation
20. All compare their explicit semantic model projections with independent
live JVM loads; frozen output captures are checked separately. Twenty-three
live JVM mutations cover source/model variations and additional admitted
forms. All four baseline consumers compiled and ran for both library and
CLI outputs with strict C++17 warnings. The CLI ran from temporary working
directories with empty `PATH` and `JAVA_HOME` unset. Repeated native library
artifacts were deterministic. No captured model is an input to compilation.

Final independent checks pass 100 Rust tests, formatting, offline all-target
Clippy, four existing Python tests plus fourteen adversarial projection
tests, reference-model checks, all 41 JVM template pairs and 315 unchanged
templates, and both retained whole-file oracles (50 legacy plus 63 M11
documentation files). Eighteen independent CLI rejection probes keep stdout
empty and preserve all existing output bytes on pre-write failure. The
independent Sol 6.1 xhigh review in `68c8749d7` reports no unresolved material
finding; see [REVIEW.md](REVIEW.md) for pinned source/tool revisions and
disposition.

Source documentation is bounded: ordinary line comments, platform sections
and admitted description/parameter/return/property/constructor blocks map
to native raw comments. Placeholders, type-local/direct parameter/accessor/
return-type documentation, block comments and field-constructor `@param`
blocks remain rejected. Constructor-parameter comments derive from fields.
Full M6 canonical/frontend parity remains open. Integer-separator mutations
match JVM bytes but retain its invalid C++ underscore spelling; mutation
byte parity is separate from baseline compilation evidence. See
[FRONTEND_ADAPTER.md](FRONTEND_ADAPTER.md) and the
[adapter oracle](tools/frontend-adapter-oracle/README.md). Implementation,
independent review, plan and verification were pushed through `cb9893cb6` to
`origin/ruscodium/rust-port`; this checklist records the confirmed publication.

## M13: reproducible Kotlin/JVM versus Rust performance comparison

Execute [the M13 contract](PLAN.md#m13-reproducible-kotlinjvm-versus-rust-performance-comparison--bounded-measurement-delivered)
using the actual JVM CLI and rebuilt optimized native `compile-cpp` path.
Keep all additions under `ruscodium/` on `ruscodium/rust-port`; preserve all
315 production templates and production compiler behavior. Roles remain
Sol 6.1 max planning, Terra 6.1 xhigh implementation, Sol 6.1 xhigh review.

- [x] Define and commit this plan/checklist before benchmark implementation.
- [x] Inspect actual JVM main/options/version and rebuild native release from
  the measured revision with `cargo build --offline --release`; record hashes.
- [x] Add deterministic workload preparation, equivalent explicit settings and
  fresh output directories, using valid real inputs plus 10/100/500-struct
  initial scaling probes. Preserve original fixtures; record any copied-default
  `field constructor(label, mapping, tags)` normalization and both validators.
- [x] Gate every workload on successful actual CLI exits and exact complete
  output inventories/bytes, including common/export files, before timing.
- [x] Run and retain a bounded pilot, select and save the final workload/trial
  matrix before measurement, and preserve slow/failure/timeout evidence with
  its elapsed bound rather than hiding unfavorable scales.
- [x] Implement a reproducible runner under `tools/performance/` for fresh
  processes with warm filesystem, monotonic wall time, user/system CPU and
  independently attributed per-process peak RSS; exclude builds/setup/parity
  verification from timings and use no oracle/export/pre-parsed timing path.
- [x] Save a seeded balanced/interleaved sequential schedule and collect seven
  or more successful trials per side/workload where the pilot permits; record
  any predeclared reduced count, warmups, every raw sample and unsuccessful run.
- [x] Verify each timed output outside its timer against the parity baseline;
  exclude failed/mismatched runs from successful comparisons without erasing
  them from the committed evidence.
- [x] Save source/dirty state, exact argv/environment, binary/jar/input/options/
  template hashes, toolchains, UTC time, OS/CPU/affinity, cgroup quotas/RAM and
  output-filesystem metadata alongside raw JSON and output-hash manifests.
- [x] Document reproducible commands and runner behavior in the tool README;
  publish `PERFORMANCE.md` with all selected workloads, output sizes, medians,
  quartiles/IQR, min/max, CPU/RSS and clearly defined JVM/Rust wall-time ratios.
- [x] Explain process/JVM/JIT/filesystem state, shared-host uncertainty, guarded
  native validation versus full JVM validation and measured-subset limits;
  keep any optional persistent-API experiment explicitly separate.
- [x] Run appropriate tooling checks and verify all 315 templates unchanged;
  obtain independent Sol 6.1 xhigh review and resolve material findings.
- [x] Finalize plan/task/review evidence, commit the reproducible results and
  leave the branch clean. Publish only within the user's existing authorization.

Measured evidence: harness `9f599c55a`, persistent setup correction
`6d37f613d`, writable-Java-home correction `311528689`, corrected report/raw
data `e8eca0c31`, independent Sol 6.1 xhigh review `7462775b8`, and chart
`cdf5ef5c1`. Production compiler code, dependencies and all 315 templates
remain unchanged from `12e45a188`. Native release was rebuilt before runs.

Five parity-gated workloads complete eight balanced randomized pairs each:
80 fresh invocations, all exact-output and logging-clean. Fresh-process
median JVM/Rust seconds are custom 1.248/0.113, corrected default
1.374/0.160, 10 structs 1.106/0.145, 100 structs 1.686/21.018, and 125
structs 2.053/33.096. Rust has lower median peak RSS on all completed
workloads. The 500-struct Rust pilot hits the 60-second bound; no matched
parity or speed ratio is claimed for that case. The predeclared fallback
125-struct case completes and remains in the report.

Separate persistent API runs on 10 structs retain ten warmups and ten
timed iterations per implementation, with all 40 output trees matching.
Post-warmup median wall is JVM 0.0313 seconds and Rust 0.1580 seconds.
These correlated within-process samples do not establish JIT steady state
or isolate startup overhead. Per-iteration CPU/RSS is not claimed.

Independent review recomputed 300 fresh metric statistics and five ratios,
warm statistics, order balance and unique destinations; rehashed 141 output
trees containing 14,018 files; checked identities and clean JVM logs; and
verified native supervisor memory attribution, exit/log handling and timeout.
The initial Python RSS/polling faults and read-only Java-home logger failure
were corrected before the accepted figures. Earlier logging-error data and
the warm setup failure remain labeled historical evidence, excluded from
final statistics. No unresolved material finding remains in this bounded
experiment. See [PERFORMANCE.md](PERFORMANCE.md),
[reproduction](tools/performance/README.md), the raw JSON and REVIEW.md.
Shared-host, tmpfs, broader JVM validation and native-subset limits remain
explicit; this is not a general language or full-parity claim. The benchmark,
corrected results, chart, independent review and verification were pushed
through `bb6fa7f59` to `origin/ruscodium/rust-port`; this checklist records that
confirmed publication.

## M14: remove repeated generation preparation

Delivered [the M14 contract](PLAN.md#m14-remove-repeated-generation-preparation--bounded-optimization-delivered)
from baseline `15b1db4c4`, preserving the current guarded subset and all
315 production templates. Sol 6.1 max planned, Terra 6.1 xhigh implemented
and Sol 6.1 xhigh independently reviewed. M13 evidence remains intact and
all new work stays under `ruscodium/` on `ruscodium/rust-port`.

- [x] Inspect graph import, class-property absence derivation, template loading,
  native resolver construction and dependency-collection indexes; define this
  bounded contract and checklist before implementation.
- [x] Commit the M14 plan/checklist before implementation.
- [x] Confirm repeated preparation with a bounded profile or temporary
  phase/count instrumentation; record source/commands and keep those runs
  outside final timing evidence.
- [x] Prepare validated graph/raw comments/computed views and native resolver
  per generation, sharing read-only state with fresh per-file engines rather
  than rebuilding graph-sized render requests; preserve preparation order.
- [x] Reuse dependency/path indexes and its native name resolver where practical
  without conflating original-model and computed rendering views.
- [x] Build class-property-name unions once per relevant view in graph import,
  adapter and generation absence derivation, preserving overlay/null/same-class
  conflict rules, unknown IDs, duplicate names and node-specific absences.
- [x] Cache lazy immutable file-partial syntax within a generation, preserving
  dynamic inline-definition precedence, collection/redefinition semantics,
  standalone calls, template-root checks and independent-call file freshness.
- [x] Remove large snapshot/AST clones required by these paths where practical;
  retain schemas, hooks, validators, error boundaries and all supported features.
- [x] Add regressions for cross-file and cross-job state isolation, changed
  templates/roots, inline-over-cached-file shadowing, forward/nested/later
  definitions and repeated calls; preserve whitespace and recursion/output limits.
- [x] Add graph regressions and adversarial probes for another same-class stored
  getter, overlay-created/null getter, different classes and malformed absences;
  retain rejected-job stdout/output preservation and path/symlink guards.
- [x] Pass formatting, offline all-target Clippy with warnings denied and Rust
  tests; verify all 41 JVM template pairs and 315 unchanged templates, retained
  whole-file/documentation goldens and native adapter/model/mutation/C++ checks.
- [x] Build separate baseline `15b1db4c4` and optimized release binaries; record
  identities and use the same host, actual raw-LIME pipeline, options, templates,
  output filesystem, JVM distribution and fresh-process measurement boundary.
- [x] Save the seeded schedule before timing: three baseline Rust samples for
  each completed custom/default/10/100/125 case, eight optimized/JVM pairs for
  all six cases, one baseline 500 attempt, and a 60-second cap on every run.
- [x] Establish six JVM workload equivalence preflights outside sample statistics,
  retain all attempts and verify every completed output against complete
  JVM inventories/exact bytes outside timers, including common/export files;
  preserve baseline 500 timeout evidence without a censored speed ratio.
- [x] Record new raw results, reproduction instructions and `OPTIMIZATION.md`
  with wall/CPU/RSS counts/distributions, baseline/optimized medians, all six
  workloads, failures, environment limits and bounded compatibility claims.
- [x] Obtain independent Sol 6.1 xhigh review of code, regressions and evidence;
  resolve material findings and rerun affected checks only as needed.
- [x] Update plan/tasks/review and usage documentation and commit tested logical
  increments.
- [x] Publish the reviewed M14 commits within the user's existing authorization.

Delivered evidence: contract `965a9ed96`; production changes `6ccea17bc`;
additional prepared-renderer tests `ec381af93`; diagnostic counts `8888fb09c`;
comparison tools `c2093ba80`, `a71c41f66` and `3f90a57a0`; report/raw results
`412913187`; counter reproduction `67d16764b`; usage/verification documentation
`0cd968bc4`; independent review `cbd13c4b0`. The implementation shares the
final rendering graph, resolver and
lazy immutable file syntax between fresh file engines, while collection retains
its own reusable original-model context. Class-property unions replace repeated
absence scans. Dynamic inline definitions retain precedence and are registered
on every encounter; independent calls retain separate caches. Public Graph
validation observes node-map mutations. Dynamic definition-body cloning remains
outside this focused reduction.

The isolated baseline diagnostic retains commands, source/executable hashes
and full-output equality with M13: 10 structs require 39 graph imports,
58 resolver constructions, 204 partial parses and 8,089,290 graph-import
absence-node probes; 100 require 219, 418, 1,734 and 2,183,649,930 respectively.
These are operation counts for the stated paths, not timed attribution or a
bottleneck percentage. That binary was excluded from timing.

All 112 scheduled attempts remain visible: 111 completed full-output matches
and the expected baseline 500 timeout at 60.009 seconds. Six independent JVM
preflights also pass. Baseline Rust has three samples per first five workloads;
optimized Rust and JVM have eight each per all six. Clean optimized source is
`ec381af93`; the baseline `15b1db4c4` executable matches M13's executable hash.
Same-host baseline/optimized median seconds are 20.844/0.089 at 100 structs
(234.7×) and 44.499/0.157 at 125 (283.2×). Optimized 500 median is 1.296 seconds
versus JVM 2.776; its capped baseline has no completed parity or numeric ratio.
Custom, corrected default and ten structs also improve; CPU/RSS distributions,
identities, schedule and all output hashes remain in the new report/raw records.
The historical M13 125-struct median is 33.096 seconds and is not used for these
new same-host ratios.

The initial full Rust suite passes 102 tests; the two additional tests and all
three prepared-renderer unit tests subsequently pass, totaling 104 unique Rust
tests checked across those runs. Final formatting and strict offline all-target
Clippy pass. Independent review passes 47 focused Rust tests, all three prepared
tests, 41 live JVM template pairs, 315-template identity and the full native
adapter oracle: ninety baseline files, actual source sets, semantic projections,
23 live mutations, deterministic output and strict library/empty-PATH CLI C++
consumers. Eighteen adversarial CLI probes preserve existing bytes and empty
stdout on rejection; they include malformed absences, cross-node stored and
overlay-null getter conflicts, and different-class independence. Four final
benchmark harness checks also pass.

Independent evidence review rehashes 117 successful output trees containing
28,786 files and recomputes 306 scalar statistics, eleven ratios and twelve
displayed metric rows. The schedule, immutable identities, timeout handling and
unequal sample counts agree with the report. No material finding remains within
the bounded M14 contract. See [OPTIMIZATION.md](OPTIMIZATION.md) and
[REVIEW.md](REVIEW.md) for scope and verification details. Shared-host variation,
two-CPU quota, 8 GiB limit, buffered tmpfs writes, synthetic scales, broader JVM
validation and fresh-process/JIT distinctions limit interpretation. M13 evidence,
all templates, supported schemas and admission boundaries remain unchanged;
full port parity and warmed-API performance remain open. The reviewed M14
implementation, measurements and verification were pushed through `347792270`
to `origin/ruscodium/rust-port`, and the remote tip was verified. This records
the confirmed publication.

## M15 / P1c.1: enum-backed synchronous exceptions and throws

Execute [the M15 contract](PLAN.md#m15--p1c1-enum-backed-synchronous-exceptions-and-throws--bounded-subset-delivered)
from baseline `0dc5def39`, preserving all 315 production templates and keeping
changes under `ruscodium/`. Sol 6.1 max plans, Terra 6.1 xhigh implements and
Sol 6.1 xhigh independently reviews. Checked boxes require recorded evidence;
removing the first exception guard alone does not establish compatibility.

- [x] Inspect the M11 smoke inventory, M12 adapter/graph boundary and upstream
  exception, throws, error-enum discovery, includes and category templates;
  choose the bounded direct-enum synchronous feature and document its limits.
- [x] Record the concrete M15 plan/checklist in `9caabcc88`, with the existing
  safe-name annotation clarification in `01d0f1223`.
- [x] Admit top-level/nested exceptions with direct nonnullable nonexternal
  enum payloads and direct nonnullable exception throws on ordinary synchronous
  instance/static class/interface/struct methods; retain all other guards.
- [x] Validate payload/throws kinds and metadata across main and auxiliary
  public models after clearing caches and fresh resolution; reject enum/exception
  aliases in these positions, scalar/struct payloads and throwing constructors.
- [x] Construct exception membership, payload/child-type edges, canonical
  ownership/reference maps, thrown wrappers/empty comments and native derived
  exception getters without JVM answers or supplied render decisions.
- [x] Extend original snapshot shape/value and semantic graph validation plus
  computed rendering views; check canonical targets, placement/nullability and
  consistency of stored/overlay exception getters instead of trusting classes.
- [x] Discover error enums through main roots/nested types exactly as the JVM
  does, including unused exceptions; preserve per-owner type order and dedupe
  shared payloads, with explicit auxiliary-ownership behavior.
- [x] Emit matching `std::error_code`, `Return<T, std::error_code>`, required
  includes, enum traits, category functions/messages and complete file sets using
  unchanged templates; preserve common/export outputs and source sets.
- [x] Keep exception declarations in model identity/ownership while emitting
  no exception files and reserving no exception output paths; retain collision
  checks for real emitted files.
- [x] Extend the explicit semantic projection and mutation tests for exception
  payloads, thrown wrappers/comments and derived exception targets; ensure
  changed or contradictory links are detected.
- [x] Add fresh JVM whole-file/model comparisons for top-level/nested and
  cross-root enum errors, shared/unused exceptions, multiple enum ordering,
  `Void`/value returns and instance/static methods.
- [x] Add live auxiliary-boundary and no-output name-collision comparisons,
  custom namespace coverage and fresh JVM comparisons after source name,
  enum-value or throw-target mutations; include the existing safe `@Cpp("Name")`
  profile on an exception without admitting another annotation family.
- [x] Compile and run library/CLI generated consumers with strict C++17 flags;
  exercise generated enum conversion/category/message and throwing-method
  `Return` success/error behavior, including configured namespaces.
- [x] Prove actual `compile-cpp` execution from a temporary directory with
  empty `PATH`/no `JAVA_HOME`, using only LIME, options and unchanged templates.
- [x] Probe unsupported payload/throws aliases, kinds/nullability, constructors,
  metadata, forged caches and malformed original/computed graph/getter links;
  preserve stdout and existing output inventories/sentinels on rejection.
- [x] Pass formatting, offline all-target Clippy with warnings denied, Rust
  and projection/tool tests, existing native adapter/model/consumer comparisons,
  retained C++ goldens, 41 template pairs and all 315 unchanged templates.
- [x] If the broader smoke matrix is rerun, keep its provenance/comparative
  first-guard report separate from focused feature acceptance; report remaining
  guards rather than treating partial group progress as whole-group parity.
- [x] Update frontend/generation/oracle docs and measured limits, complete the
  independent Sol 6.1 xhigh review, fix material findings and rerun affected
  checks, then commit the verified bounded increment.
- [ ] Publish the reviewed increment under the existing branch authorization
  and verify the remote branch tip.

Delivered evidence: production `3d07f3232`, focused oracle `b27701d3b`,
comparative report `77bdee61e` and independent review `f518651d6`. Eight fresh
JVM cases compare 196 complete files and model projections; twelve strict
C++17 consumers compile and run across JVM, native library and empty-PATH CLI
outputs for four cases. This includes actual default/custom options, class/
interface/struct methods, exception-only input, shared/unused and ordered nested
enums, auxiliary discovery, safe exception names and three live source
mutations. See the [oracle](tools/enum-errors-oracle/README.md) and its pinned
[evidence](tools/enum-errors-oracle/evidence.json).

All 106 Rust tests, formatting, offline all-target Clippy, fourteen projection
and four existing Python tool tests pass. Retained live checks pass the 90-file/
23-mutation frontend oracle, 50 whole-file and 63 documentation outputs with
consumers, 41 template pairs and 315 unchanged production templates. Independent
review reproduced the focused evidence, added forty rejection probes preserving
whole output inventories, two positive job checks, four fresh JVM cases (84
files) and public-model cache mutation checks. No material finding remains.

The broader snapshot matrix keeps its original one exact complete group and
twelve guarded complete-group rejections, plus two exact isolated documentation
files (64 accepted files). All fifteen case and environment provenance checks
match M11. Moving six first exception guards exposes DART, constant references,
Markdown and ASYNC; no additional complete-group parity is claimed. Broader
frontend/C++/platform coverage remains deferred below. Publication is recorded
separately after remote verification.

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
