# Ruscodium: a staged Rust port of Gluecodium

## Goal and source of truth

Port the Gluecodium compiler itself to Rust: read LIME IDL, construct and validate
the language-independent model, and generate existing target languages. This is
not a proposal to add Rust bindings to the Kotlin compiler. Keep all committed
work for the port under the repository-root `ruscodium/` directory and leave the
existing implementation usable as a reference.

Planning baseline: commit `2044ae5c73e8b9521fac6dec6cd6133086dd4136`.
The linked Claude page could not be retrieved in this environment. The user
subsequently supplied its answer as text; that supplied analysis now informs the
parity strategy below. This does not imply the linked page was inspected.
Repository code, grammar, examples, and tests remain the compatibility oracle.

## Findings and scope

The existing production implementation comprises 251 Kotlin source files and 315
Mustache templates across `lime-loader`, `lime-runtime`, and `gluecodium`.
There are 345 checked-in `.lime` files (18,471 lines) across smoke tests,
functional tests, CMake tests, and examples. Gluecodium generates C++ API code,
Java/Kotlin plus JNI, Swift plus CBridge, and Dart plus FFI. Replacing all of those
with verified compatibility is a migration, not a single small translation.

The supplied analysis estimates 35–45 thousand lines of Rust and describes
about 318 templates and 2,500 `resolveName` uses at an older revision. Those are
planning estimates, not this checkout's inventory or a promised implementation
size. Its central finding applies here: the difficult part is preserving the
Trimou/Mustache object-property and helper behavior, name resolution, and exact
generated whitespace, rather than merely translating Kotlin data classes.

The first executable deliverable is a useful native compiler preview:

1. A Rust library and CLI with a real LIME frontend covering the repository's
   complete declaration and literal syntax.
2. A multi-file model with source locations, annotation/documentation retention,
   import and type resolution, and an explicitly documented set of semantic checks.
3. Deterministic JSON model output for inspection and future differential tests.
4. A guarded, standalone C++17 declaration backend for common interfaces and value
   types, exercised by compiling and using generated declarations.
5. Tests against the existing LIME corpus and targeted comparisons against the
   installed JVM implementation where available.
6. A reproducible static inventory of template property paths, helpers, and
   partial dependencies to make the subsequent compatibility work concrete.
7. An experimental JVM reference-model graph exporter to start the canonical
   model investigation without changing the existing Kotlin loader.

This first release does **not** claim drop-in Gluecodium compatibility. In
particular, generating a standalone C++ interface does not imply compatibility
with Gluecodium's JNI, CBridge, Dart FFI, or runtime ABI. Unsupported backend
features must produce a diagnostic before any outputs are written, rather than
silently dropping declarations or changing their meaning. The broader roadmap
below remains tracked after this deliverable works.

The native preview was already underway when the user supplied the analysis.
Complete this independently useful milestone, then use the model-export and
backend-first sequence below for exact parity. The preview's frontend, JSON
output, and standalone declarations do not substitute for a Kotlin model
exporter, a canonical schema adapter, or byte-for-byte backend comparisons.

## Reference sources

- [Architecture](../docs/internal/architecture.md),
  [loader](../docs/internal/lime_loader.md),
  [resolution](../docs/internal/reference_resolution.md), and
  [validation](../docs/internal/validation.md).
- Authoritative lexical and syntactic rules:
  [`LimeLexer.g4`](../lime-loader/src/main/antlr/LimeLexer.g4) and
  [`LimeParser.g4`](../lime-loader/src/main/antlr/LimeParser.g4).
- Semantic model and name lookup:
  [`lime-runtime`](../lime-runtime/src/main/java/com/here/gluecodium/model/lime/),
  especially `LimeAmbiguityResolver.kt`.
- Existing validators, C++ name rules, and templates under
  [`gluecodium/src/main`](../gluecodium/src/main/).
- [`Calculator.lime`](../examples/calculator/lime/Calculator.lime), smoke
  fixtures, and functional inputs are acceptance examples, not specifications
  to replace with a smaller invented language.

## Architecture

Use a single Cargo package containing a reusable library and a `ruscodium`
binary. Prefer a small dependency set, with checked-in `Cargo.lock`; `serde`
and `serde_json` are reasonable for the inspectable model. No JVM subprocess
may be required by the Rust compiler. The JVM tool is only a test oracle.

Suggested module boundaries:

| Module | Responsibility |
| --- | --- |
| `source` / `diagnostic` | Source identity, byte spans, line/column rendering, structured errors |
| `lexer` | Tokens, newline boundaries, quoted identifiers, strings, comments, numbers |
| `parser` | Recursive-descent implementation of the checked-in LIME grammar |
| `model` | Owned declarations, type references, annotations, values, documents |
| `resolve` / `validate` | Symbol indexing, scope/import lookup, cycles, semantic checks |
| `generator` | Generated files in memory; deterministic JSON and guarded C++ emitters |
| CLI / IO | Sorted input discovery, options, pipeline execution, safe output writing |

Represent declarations and references without reference-counting cycles: use
stable indices or full symbol paths for resolved targets. Preserve original
spelling and spans alongside resolved identities. Separate parsing from name
resolution so files may refer forward or across input boundaries.

Use a static registry of generator traits instead of Java `ServiceLoader`.
Handwritten recursive descent, optionally with a lexer such as `logos`, avoids
depending on an immature Rust ANTLR target; lexical-library choice is an
implementation detail provided the checked-in grammar remains authoritative.
Treat name rules, options/configuration, output caching, and `Skip`/`EnableIf`
filtering as explicit compatibility modules, not template-engine side effects.

The user has chosen to keep Mustache. Preserve the original production
templates unchanged and implement their existing Trimou-compatible syntax,
helpers, partials and whitespace behavior in Rust. P1a now uses a custom Rust
compatibility runtime; retain that measured boundary as coverage expands.

## First implementation milestones

### M0: establish the migration record

Create this plan and `TASKS.md` before implementation, commit them, then execute
the task list. Record evidence and scope changes as work proceeds. Use the
user-requested roles: Sol 6.1 at max effort for planning, Terra 6.1 at xhigh
effort for the continuation implementation, and Sol 6.1 at xhigh effort for
review. Commit finished logical increments. The user has subsequently authorized
pushing the incremental work to `ruscodium/rust-port`; this does not authorize
replacing the JVM compiler or claiming parity before the corresponding evidence
exists.

### M1: complete syntax frontend and source-aware model

Implement all declaration forms in `LimeParser.g4`: packages and explicit
imports; open classes, narrow interfaces, inheritance and nested declarations;
structs and fields; functions, named constructors and field constructors;
properties and accessor annotations; enums, constants, aliases, exceptions,
and lambdas with named or positional parameters. Retain external descriptors,
annotations on declarations and type references, return/throws documentation,
and declaration comments. Local `#` comments need not become model nodes.

Cover built-in, user-defined, generic and nullable types. Parse strings and
multiline strings, escapes, signed/underscored numeric literals, special floating
values, duration units, enum/constant references, positional enum values,
struct/list/map initializers, and backtick identifiers. Do not use token skipping
as a substitute for parsing a construct. Reject malformed source with a file,
line, column, and useful expected-token message. Explicitly document any
deliberate grammar deviation discovered by tests.

### M2: model loading, resolution and core validation

Discover `.lime` inputs recursively in deterministic order, support multiple
input files/directories and auxiliary inputs, and deduplicate inputs. Auxiliary
declarations participate in lookup but are not generated.

Build a global symbol index, detect duplicate non-overload declarations, and
resolve names after all files have been parsed. Match Gluecodium lookup:
collect candidates from matching explicit imports **and all enclosing paths,
including the root**, deduplicate the targets, and report ambiguity if more than
one remains. Do not assume nearest-scope shadowing. Validate imports, forward
and nested references, type-target kinds, alias cycles, and inheritance kinds
and cycles. Distinguish valid overloads from duplicate function signatures,
including alias-equivalent types where supported.

Port a useful, named set of independent checks: duplicate parameters/fields/
enumerators, invalid `Void` and nullable-`Void` positions, throws targets,
field-constructor references, and obvious invalid defaults such as `null` for a
non-nullable field. Add constant/default reference checks where implemented.
Maintain a precise compatibility table: semantic validation in the preview is
not equivalent to all Kotlin validators. JSON export should preserve parsed
features even when no code backend supports them.

### M3: native CLI and inspectable output

Provide help/version, repeated inputs and auxiliary inputs, output directory,
validation only, syntax-only/model inspection for corpus work, and explicit
generator selection. Support familiar single-dash Gluecodium spellings for the
implemented common flags, or clearly list aliases in help. Reject unknown
options and unsupported generator names with nonzero exit codes. Require an
explicit output directory for generation; validation must not write files.

JSON should have a versioned schema and stable ordering and include parsed
declarations, type/literal structure, annotation/documentation metadata, source
positions, auxiliary status, and resolved symbol identities. Use the same
library pipeline from the CLI, tests, and generators.

This is the preview's inspectable model format. The experimental JVM snapshot
described in P0 is a separate representation. P1a imports that bounded snapshot
in Rust. M12 now adapts the native model to the existing C++ compatibility
backend for its guarded subset. A template-complete canonical schema and
full-fidelity native adapter remain planned work; neither M10's snapshot output
nor M12's bounded path supplies that complete canonical/frontend boundary.

### M4: useful, honest C++17 generation

Generate standalone declarations for ordinary classes/interfaces (virtual
methods and destruction, named factory declarations, property accessors),
structs with fields, enums, aliases, lambdas, and basic constants/defaults.
Support nested declarations and cross-file dependencies in a deterministic
order. Map primitive types, strings, blobs, common containers, optionals, and
class/interface references to appropriate standard-library types. Document
naming and namespace rules and provide a namespace option if feasible.

Handle declaration ordering and forwards correctly for supported inputs; reject
unsatisfiable by-value dependency cycles. Detect output path/name collisions.
Implement or explicitly reject code-affecting annotations and external
descriptors. Language-specific metadata irrelevant to C++ may be retained
without affecting C++ generation, but generic or C++ attributes must not be
silently ignored. Likewise, reject unsupported throwing/error-code behavior,
runtime-dependent types, or initializers rather than inventing compatibility.

The calculator must at least parse, resolve, validate under the documented
checks, and export JSON. Its throwing methods can remain an explicit C++ backend
limitation until Gluecodium's `Return`/error-code runtime is ported. Compile and
use a separate representative generated C++ fixture with classes/interfaces,
structs, collections/optionals, nesting, aliases, and multiple input files.
Include a checked-in repository fixture in C++ acceptance where its features
fall within this backend's contract.

### M5: verification, review and handoff

- `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, and
  `cargo test` from `ruscodium/`.
- Parse all 345 baseline `.lime` files individually, with exact file count
  assertions or an explained inventory; no blanket ignores or exclusions.
  Parsing them as a single model is invalid because many fixtures deliberately
  reuse qualified names in separate test scenarios.
- Resolve/validate coherent fixture groups separately, including the calculator
  and selected real functional/smoke groups with their auxiliary sources.
- Test malformed strings/comments/declarations, unresolved and ambiguous names,
  import collisions, duplicate declarations/signatures, alias/inheritance
  cycles, and unsupported-backend errors. Verify failure produces no partial
  generated output and repeated output is deterministic.
- Compile generated C++ with `-std=c++17 -Wall -Wextra -Werror` where a compiler
  is available and execute a small program using generated declarations.
- Compare selected validation successes and failures with the installed JVM
  Gluecodium (`-input ... -validate`), especially import-vs-local ambiguity.
  Report differences honestly; passing parser corpus tests is not output parity.
- Run the requested independent review, fix material findings, update tasks and
  compatibility documentation, and commit the tested result.

The delivered [`tools/compare_validation.py`](tools/compare_validation.py) makes
the acceptance comparison reproducible: 58 cases comprising nine core cases
and 49 smoke groups, with four known directional differences recorded rather
than hidden. It also records JVM stack-overflow failures on cycle cases. This
checks acceptance outcomes; it does not establish diagnostic, crash-behavior,
model, or generated-output parity. Keep its results current as review fixes
change either implementation's outcomes.

### M6: map the template compatibility surface

Delivered [`tools/template_surface.py`](tools/template_surface.py), scanner
tests, and [`TEMPLATE_SURFACE.md`](TEMPLATE_SURFACE.md). The inventory scans the
checkout's 315 templates rather than hardcoding the supplied analysis's counts.
It reports candidate property paths, helper invocations and selector arguments,
partial/include references and inline definitions, and dynamic constructs that
cannot be resolved statically. It covers `resolveName`, `prefixPartial`,
`ifPredicate`, `instanceOf`, `sort`, `filter`, and `set`; the report records
current counts and the corpus hash for reproduction.

The report is an implementation inventory, not a working template engine or
proof that every Kotlin reflective access has been reproduced. Keep extraction
deterministic and test nested sections, quoted arguments, comments and partial
syntax so the report can guide later typed Rust template views.

## Exact-parity migration after the native preview

The following phases adopt the supplied analysis's backend-first approach.
P0 has delivered bounded investigation tooling, P1a a native template/runtime
slice, M8 a bounded native C++ name resolver, M9 native C++ predicates and
declaration sorting, M10 whole C++ file sets for a guarded snapshot subset,
and M11 bounded native documentation with a reproducible smoke inventory.
M12 below delivers a bounded adapter from the existing Rust frontend to that
working compatibility backend, including bounded source documentation. The
complete canonical boundary, remaining C++ features and platform backend phases
remain incomplete until their own
acceptance evidence exists.

### P0: experimental snapshot delivered; canonical boundary incomplete

Delivered [`tools/reference-model/`](tools/reference-model/README.md): a Java 17
tool that calls the unchanged installed Kotlin loader and serializes a versioned
JSON graph. Instance IDs preserve sharing and cycles; properties and map keys
are sorted, lists retain loader order, and repository source paths are normalized.
The bounded property selection reads public getters backed by model fields,
plus explicitly allowed `LimeTypeRef.type` and `LimeElementRef.element` semantic
edges; attributes use their typed public API. It excludes private implementation
fields and most computed getters, so computed documentation and external
descriptor data needed by templates can be absent.

Verification covers byte-identical calculator snapshots from separate JVM
processes with the same distribution/inputs, main and auxiliary sources,
resolved reference targets, and syntax/unresolved-reference failures before an
output file is opened or truncated. This is an experimental reference snapshot,
not a complete template model or a compatibility guarantee. Its README defines
the exact property policy, schema and reproducibility limits.

Remaining work: define and test a template-complete canonical schema, account
for omitted computed data, and capture canonical goldens for coherent smoke
fixtures. Record upstream commit, generator configuration and fixture grouping
with each golden. Implement and test an explicit adapter from the preview model;
P1a's Rust importer handles the existing bounded snapshot, not a complete
canonical model. The snapshot's traversal IDs are not a promise of stable
semantic identities across model revisions. The export tool may use the JVM,
while native rendering already consumes its snapshots without starting a JVM.

### P1a: executable Mustache and snapshot compatibility slice — bounded milestone delivered

Delivered a custom native Rust runtime for a bounded slice of the existing
Trimou dialect. It reads all 315 unchanged production `.mustache` files from an
explicit template root and does not start a JVM. The installed JVM engine is
an independent fixture-generation oracle. [TEMPLATES.md](TEMPLATES.md) defines
the implemented contracts and limits; [the oracle README](tools/template-oracle/README.md)
records the current fixture matrix, counts and provenance.

The delivered slice comprises:

1. An explicit syntax tree that parses the entire production template corpus.
   It handles quoted/literal/positional/named arguments, dotted and bracketed
   keys, escaped and unescaped interpolations (escaping is disabled upstream),
   Trimou comments, ordinary and inverted sections, partials, and
   forward-referenced `{{+name}}` inline partial definitions. Central parser
   preflight checks configured helper minimum arities and tag forms, `set`'s
   named arguments and `setJoin`'s delimiter, even inside inactive branches.
   Parsing all 315 templates establishes syntax coverage, not their complete
   dataflow or helper/view compatibility.
2. A public `Graph` API importing `gluecodium.reference-model.snapshot` version
   1 as an identity graph. It validates schema/version, IDs, classes, references
   and supplied overlays before rendering; graph edges preserve sharing and
   cycles without recursive model copying. Null/scalars/lists/maps and enum
   values retain the snapshot's shapes. This is distinct from preview-model
   JSON and from the unfinished complete canonical adapter.
3. Explicit stored-property and bounded native views for maps, lists, strings,
   enum/class identity and the case-insensitive `LimeAttributes` Map interface.
   Measured computed getters use `property_overlays`; measured nonexistent
   getters use `absent_properties`. Missing plain-map keys follow the measured
   Trimou behavior, while an unavailable model property remains a strict
   unsupported-view error. Arbitrary Kotlin reflection, computed documentation
   and platform descriptors are not supplied by this boundary.
4. Context lookup, section iteration and `iter` metadata, scoped `set`,
   `if`/`unless` with their different multiple-argument defaults, named/inline
   partials, `prefix`/`prefixPartial`, `join`/`joinPartial`, class-name tests and
   additional measured helpers documented in `TEMPLATES.md`. Selected scope,
   standalone tags, indentation, prefix trimming and final newlines have exact
   JVM fixtures. Legacy requests replay `resolveName` results; M8 adds explicit
   native C++ naming as described below. M9 adds separate predicate/sorter
   opt-ins; disabled providers retain measured replay. Unknown selectors and
   unsupported executed helpers, options and views fail explicitly.
5. Public library `parse`, `Graph` and `render` entry points and the native
   `render` CLI below. Requests are validated and rendered in memory before
   output is opened, preserving an existing output file on import/render
   failure. The CLI remains experimental tooling separate from the standalone
   `cpp` preview generator; a standalone CLI graph inspector is still pending.
6. A JVM oracle under `tools/template-oracle/` using the actual unchanged
   Kotlin engine and registered helpers. Its checker verifies all 315 source
   templates against the installed jar, reproduces request and UTF-8 output
   bytes, and checks selected compile/render failures at their measured phase.
   Model cases use identity snapshots, observed public getters/absences and
   actual C++ resolver, predicate and sorter results. The oracle does not
   substitute rendered output for a helper result or copy production templates.

The Rust CLI and JVM oracle use this shared request protocol:

```text
ruscodium render --templates DIR --request FILE [--output FILE]
```

The request has `schema: "gluecodium.template.render-request"`, `version: 1`,
`template` (extensionless template-relative name), `data` (root render value),
an optional `snapshot` containing the existing version-1 reference document,
optional `property_overlays`, optional `absent_properties`, optional `hooks`,
and the M8 `native_cpp` opt-in described below and in [TEMPLATES.md](TEMPLATES.md).
Plain JSON helper cases can omit the snapshot. Values use the snapshot's existing
reference, enum, scalar, list and map shapes. A reference in `data` or an overlay
resolves against the embedded snapshot and retains its instance identity.
`property_overlays` maps snapshot node IDs to property maps; the oracle may add
measured public computed getter results without changing snapshot version 1 or
pretending those getters were present in the original bounded exporter.

`absent_properties` maps snapshot node IDs to lists of property names, for
example `{"n4": ["propertyElement"]}`. This additive optional field records
only model properties whose public JVM getter is actually absent. It permits
the runtime to return Missing for that measured absence, so unqualified lookup
can continue through enclosing contexts while explicit `this.propertyElement`
remains missing/null. An omitted computed getter that actually exists must have
its measured result exported as an overlay; recording absence or inventing a
null value would hide an unsupported view. Validate that every declared node ID
exists, names are distinct and each absent property is disjoint from stored
properties and overlays on every node of that class.
The oracle must propagate throwing getters instead of treating them as absent.
An unmeasured missing model property remains a strict unsupported-view error.

For legacy replay requests, `hooks.names` is a list of
`{resolver, mode, receiver, result}` records, with
mode `name`, `getter`, `setter` or `ref` and a string-or-null result.
`hooks.predicates` is a list of `{name, receiver, result}` records with boolean
results. `hooks.sorters` is a list of `{name, input, result}`
records containing ordered input/result value lists. Receivers and list entries
are graph values; equality preserves referenced instance IDs. Identical replay
entries are permitted, while contradictory duplicates and malformed values
fail. Unknown selector names and missing requested results fail explicitly.
A null receiver to `resolveName` in replay mode needs evidence of the requested
resolver/mode in `hooks.names`, without an invented receiver-specific null result.
Native requests register their supported selectors directly and reject nonempty
`hooks.names`; they do not use a captured name result or fall back to replay.

Optional `hooks.registered_predicates` contains distinct, nonempty names from
the actual Kotlin predicate catalog. A measured receiver-specific predicate
entry also establishes that its name is registered. The separate catalog
permits an empty filter when no predicate invocation was observed; it must not
be replaced by fabricated per-receiver results. With neither catalog evidence
nor an observed result for a name, even an empty filter fails. Every evaluated
receiver still needs its measured boolean result. This strict rejection of
unknown predicates is intentional even where JVM filtering would skip them.
The serialized hooks remain an explicit offline replay boundary for legacy
requests. M8 ports the bounded native naming surface below; M9 adds explicit
native C++ predicates and declaration sorting. Broader naming and future
helper-provider interfaces remain implementation work.

The real-template matrix covers `cpp/CppEnumeration`, `cpp/CppTypeAlias`,
`cpp/CppFunctionSignature` and `cpp/CppReturnType` with unchanged transitive
partials, plus configured `cpp/common/Export`. Actual JVM-loaded models cover
enumerators and literal values, a list alias, multiple parameters, nullable
alias/enum references and throws, const/static/noexcept attributes, a callback
parameter and ordinary returns. The oracle README records the exact cases,
default naming configuration and direct-model-root ambient-context limits.
Keep uncovered model/configuration combinations open as the matrix expands.

The bounded milestone has corpus parsing, identity/cycle and invalid-import
checks, focused helper/whitespace comparisons, selected real-template exact
bytes and pre-write failure checks. Corpus hashes and oracle distribution
provenance are recorded in the linked inventory and oracle documentation;
verification and independent review evidence is maintained in
[TASKS.md](TASKS.md) and [REVIEW.md](REVIEW.md). These results establish the
selected engine/view contract. P1a's replay evidence does not establish native
naming; M8 supplies separate native naming comparisons below. Neither milestone
establishes canonical model completeness, complete C++ file sets or runtime/ABI
parity.

Full Trimou syntax validation and consistent source-position diagnostics, the
standalone CLI graph inspector, and unimplemented helper/view contracts remain
open within this experimental runtime. M10 below delivers a guarded whole-file
C++ backend using these native providers. The native frontend-to-canonical
adapter and complete model/helper/backend coverage remain pending.

### M8 / P1a.1: strict native C++ naming — bounded implementation delivered

Delivered a separate Rust name resolver over the imported identity graph in
[`src/template/native_cpp.rs`](src/template/native_cpp.rs), with JVM-generated
fixtures in commit `931251088` and native implementation in `5d9828539`.
It computes a measured subset of C++ names without recorded name results and
keeps all 315 production Mustache templates unchanged. This continues P1a;
the complete P1b backend, canonical frontend adapter and whole-C++ runtime parity
remain open. M10 adds whole-file output evidence for its guarded subset below.

Sol 6.1 max committed the initial plan/checklist in `1b456d4a2` before code;
Terra 6.1 xhigh owns implementation and evidence, and Sol 6.1 xhigh independently
reviews the resulting behavior. The independent review disposition and final
verification evidence are tracked in [REVIEW.md](REVIEW.md) and
[TASKS.md](TASKS.md). All changes remain under `ruscodium/`.

#### Request and resolver contract

The optional `native_cpp` object extends the existing version-1 render request.
Its presence selects native names; omission retains the existing replay contract.
The options are `root_namespace` and `internal_namespace`, each an array
of namespace components, defaulting to empty arrays as in `GeneratorOptions`.
For the existing oracle configuration use
`native_cpp: {"root_namespace": [], "internal_namespace": ["internal"]}`.
Types, ASCII namespace components and unknown option keys are validated before
rendering.
An empty object is an explicit opt-in, not a request to replay captured names.

Native mode rejects nonempty `hooks.names` and never consults name recordings on
a success or unsupported-receiver path. Differential tests use recorded name
cells solely as expected values, outside the request being rendered.
Existing predicates, sorters, registration catalogs, property overlays and known
absences remain explicit replay/measured boundaries. They do not become native
because names are native. Native registration supplies selectors `""`, `"C++"`
and `"FQN"` without fabricated hook entries. Measured helper argument, mode
normalization and null-receiver behavior are preserved; unsupported selectors
and modes fail.
The upstream `ref` mode is not implemented by these C++ resolvers and remains an
explicit error. FQN uses `CppFullNameResolver` semantics, not a qualified version
of the C++ type-expression resolver.

Helper dispatch and native name-rule/type calculations are separate. The resolver
uses actual node classes, `LimePath` head/tail/disambiguator, reference edges and
attributes, with an index of available parent nodes. It requires all traversable
parents needed by `CppNameCache`. A selected-object snapshot can omit its owning
container: missing parents are unsupported context, never evidence of default
parent names or attributes. The new native JVM fixtures snapshot the real full
model and retain the selected render root in `data`; no parent nodes or resolved
name strings are synthesized. [TEMPLATES.md](TEMPLATES.md) documents the public
single-receiver API as well as render-request configuration.

#### Bounded naming surface

The native module implements the checked-in `namerules/cpp.properties` and
measured Kotlin `NameHelper` behavior for ASCII names, including underscores,
mixed case/acronyms and getter prefixes. Unmeasured Unicode casing and
configurable naming files are explicitly unsupported.

The measured matrix covers ordinary named declarations, parameters, fields,
constants/enumerators, root/package/nested qualification, enum/type-alias names,
`LimeBasicType.TypeId`, type references and return types. It checks exact C++
primitive/string/blob/date/duration/locale type spellings, list/map/set spacing
and hash selection, nullable wrappers, class/interface shared pointers, exception type
mapping, alias identity and alias-aware actual-type decisions. Aliases retain
their names where the Kotlin resolver does. Cycles and missing required facts
produce bounded diagnostics.

The slice also covers measured ordinary literals and constant references, property
getters/setters and field accessors where real parent context establishes
`@Cpp(Accessors)`, including boolean getter prefixes through aliases. Supported
attribute interactions include `@Cpp(Name)`, accessor `@Cpp(Name)`, `@Cpp(Type)`
and `@Optimized` where the source resolver uses them. The tests retain upstream
errors for element/rule combinations unsupported by the default rule set.

At M8, nonempty comment processing, external descriptors, custom naming files
and complex defaults were deferred. Its legacy measured-empty path resolves a
comment to the empty string from its actual `isEmpty` fact; a missing comment
fact is unsupported. M11 below adds a separate bounded raw-documentation profile.
Resolved C++ comment strings are not native projections. Date/locale/duration,
special and aggregate literal forms beyond the supported literal matrix produce
an explicit unsupported diagnostic. Unsupported attributes or unavailable
required model facts fail before any output write; replay is never the fallback.

#### Evidence and remaining acceptance

[`tests/native_cpp_names.rs`](tests/native_cpp_names.rs) compares every recorded
name cell with the native resolver, asserting exact string/null results for the
supported set and explicit rejection reasons for the remainder. Those reasons
include missing owners in older selected-object snapshots, nonempty comments
and unsupported `@Cpp(Attribute)` handling. The full-model JVM matrix separately
proves actual enclosing names/attributes, nonempty root/internal namespaces,
types, aliases, literals and accessors. Current counts and reproduction settings
belong to the [oracle documentation](tools/template-oracle/README.md) and tests.

Four genuine JVM-loaded comment-free cases render unchanged
`cpp/CppEnumeration`, `cpp/CppTypeAlias`, `cpp/CppFunctionSignature` and
`cpp/CppReturnType`, including executed partials and supported function
attributes. Their native tests remove all name hooks and compare exact output
bytes with the JVM. Existing comment-bearing replay fixtures remain available.
These comparisons prove a native naming slice, not full-file C++ parity.

Keep invalid configuration/selectors, mixed native/name-hook requests, missing
parent or external facts, unsupported comments/attributes/defaults and cyclic
dependencies covered by strict errors and output-preservation regressions.
Retain formatting, offline Clippy, Cargo, Python/reference-model, JVM fixture
reproduction and 315-template equality checks, together with the preview corpus
and C++ consumers. The independent review must resolve material findings and
record its final verification before final review approval is claimed.

### M9 / P1a.2: strict native C++ predicates and declaration sorting — bounded implementation delivered

Planning baseline: `96b7c3421`; the plan/checklist was committed in `04058aaaa`
before implementation. The separate Rust provider in
[`src/template/native_controls.rs`](src/template/native_controls.rs) implements
the eleven C++ predicates and default declaration sorter over the imported
identity graph. Implementation began in `65b9c483a`; strict model/reference
guards and raw constructor/default handling were completed through `2d4302b58`.
The renderer whitespace correction in `3c81755f5` permits the unchanged original
`cpp/CppStruct` and `cpp/CppClass` partials to match the JVM byte-for-byte.
Field-bearing fragment support and its full-model JVM proof are committed in
`8eecc1b3b` and `30562b676`.

The bounded deliverable combines native names, predicates and sorting in
comment-free, full-model fragments with **all hooks removed**. All changes
remain under `ruscodium/`; the 315 production templates remain unchanged.
Sol 6.1 max owns planning, Terra 6.1 xhigh implementation and evidence, and
Sol 6.1 xhigh independent review. The acceptance evidence, final verification
and review disposition are tracked in [TASKS.md](TASKS.md),
[REVIEW.md](REVIEW.md) and the
[oracle documentation](tools/template-oracle/README.md#native-c-predicates-and-sorting).
This is not header/file-set generation, runtime/ABI compatibility, or a frontend
adapter.

#### Explicit dispatch and strict input boundary

The `native_cpp` object now accepts boolean `predicates` and `sorters`, both
defaulting to `false`. Presence of the object continues to select native
names as in M8. `native_cpp: {}` and old requests therefore retain their current
predicate/sorter replay behavior; omission retains all legacy behavior.
Nonboolean options and unknown keys fail before rendering. The
`predicates: true` provider registers the actual eleven C++ predicate names
directly and rejects nonempty
`hooks.predicates` **and** `hooks.registered_predicates`. With `sorters: true`,
the provider registers only the default sorter selector `""` and rejects nonempty
`hooks.sorters`. Empty arrays or omitted hooks are allowed. Each enabled provider
rejects unknown selectors even for empty inputs and never consults recorded
results or falls back to replay for unsupported receivers. Disabled
providers retain their existing strict replay contract.

The algorithms use stored model facts, resolved type/element edges, the actual
parent/reference index, and attributes. Native predicates and sorting do not
use overlaid `actualType`, `exception`, `uninitializedFields`,
`allFieldsConstructor`, collected-import sets, dependency lists, or helper result
booleans as substitutes for their algorithms. Alias targets, function exceptions,
uninitialized fields and field-constructor membership derive from raw references.
Generic children derive from actual list/set element or map key/value fields,
not an overrideable `childTypes` projection. Required shapes, node/type kinds,
membership, ownership and lazy field-reference targets are checked, with bounded
depth and cycle guards. Missing or malformed required facts produce an explicit
error. Ordinary wrong receiver kinds retain Kotlin's `false` behavior where no
model fact is needed.

Measured getter overlays remain permitted for separately documented template
views. The added `LimeNamedElement.name`/`fullName`,
`LimeStruct.uninitializedFields` and `LimeFieldConstructor.fields` overlays come
from actual public JVM getters and are documented in the oracle evidence.
Their presence does not replace native algorithms. Computed sorted declaration
lists, predicate answers and dependency/import collections are not imported.
Snapshot schema version 1, reference identity and strict absence handling remain
unchanged.

M9 retains M8's comment boundary: an observed `LimeComment.isEmpty == true`
establishes a comment-free input, with raw `isExcluded` and deprecation attributes
still honored. Required nonempty or unavailable comment content is unsupported;
the provider does not invent platform text from omitted private tagged sections.
`hasAnyComment` can prove true through an independent valid exclusion,
deprecation or C++ non-null-warning operand even when another operand has
unsupported nonempty text. This exception is limited to uncertain text;
malformed/missing required model facts remain errors. Exclusion applies only
where the Kotlin algorithm reads it, not to return/parameter/thrown-type or
owning-struct constructor comments. Raw comments, placeholders and Doxygen
processing were deferred at M9; M11 below adds a bounded native profile.

#### Implemented predicate algorithms

The source of truth is `CppGeneratorPredicates.kt`, together with
`CppNameResolver.needsRefSuffix`, `CommonGeneratorPredicates`,
`CppImportsCollector.collectTypeRefs` and `LimeTypeHelper.getAllTypes`.
All eleven selectors are implemented within the facts/comment boundary above:

| Selectors | Required native behavior |
| --- | --- |
| `needsRefSuffix`, `needsNotNullComment` | Follow alias-resolved actual types, nullability, the String `@Cpp(Type)` exception and the source's primitive/enum/container distinctions. |
| `hasAnyComment` | Preserve function return/parameter non-null warnings, exclusion and deprecation; inspect field-constructor/owning-struct comments where relevant; reject required unavailable/nonempty text. |
| `hasDefaultConstructor`, `hasPartialDefaults`, `needsAllFieldsConstructor` | Derive field defaults and explicit field constructors; preserve zero-field constructor suppression, all-fields matching and immutable descendants. The C++ default-constructor traversal follows actual struct field types, whereas common `hasImmutableFields` unwraps list/set elements and map values; these are distinct algorithms. |
| `needsPointerValueEqual`, `needsRawPointerEqual` | Follow alias targets, class/interface equatability and nullable field references, including the source's ordering of these conditions. |
| `isUsedInAnotherInnerClasses`, `needsInnerForwardDeclarations` | Traverse actual nested types and the source collector's constants, struct fields, function parameters/returns/exceptions, class properties, aliases, lambdas and container child references. Preserve sibling identity, parent-kind checks and enum-exception handling; this is not inheritance reachability. |
| `asyncFunNeedsSynchronousVersion` | Evaluate Java, Kotlin and Swift skip attributes on the function and its actual enclosing named elements; return true when at least one platform remains unskipped. |

Bounded visited sets permit legal recursive struct traversal; malformed
alias/parent/container cycles and incomplete required context fail explicitly.
M8's supported naming attributes and raw-comment contract remain bounded.

#### Exact default sorter

The provider implements `TopologicalSort.kt`. The actual C++ registration first
filters the helper's concatenated input to `LimeNamedElement` instances.
Dependencies are keyed by full name and limited to names present in that input;
they recursively visit generic type-reference children, then include the
referenced type's own full name. Aliases retain their referenced
identity: an alias declaration contributes its own target dependency when
processed separately. Each element's self dependency is removed.

Dependency collection dispatches as upstream: typed elements use their
type reference; structs use fields, functions and constants; aliases use their
target type reference; functions use parameter, return and exception error-type
references; lambdas use parameters and return; other named elements contribute
none. Inheritance and arbitrary nested declarations do not add edges here.
Each iteration selects the **first eligible element in original input order**,
removes its full name from all remaining dependency sets, and reports
`Cycle detected in C++ elements dependencies.` if no element is eligible.
Independent/tied elements retain input order, and already sorted inputs are
idempotent. Duplicate input full names, including repeated instances, are a
strict input error; the provider does not silently deduplicate or reproduce the
upstream duplicate-instance pseudo-cycle behavior.

#### Oracle and completion evidence

[`tests/native_cpp_controls.rs`](tests/native_cpp_controls.rs) inventories every
actual recorded predicate cell and sorter record across the fixtures, invoking
native providers with recordings used only as expectations. The expanded
inventory has 1,095 exact predicate matches, four explicitly rejected
nonempty-comment cases, and 15 exact sort records. The JVM full-model matrix
exercises all eleven selectors through aliases, nullable and non-nullable type
refs, equatable classes, defaults, zero/partial/all-field constructors, nested
immutable structs, sibling inner references and inherited platform skips.
Wrong receiver kinds and missing/malformed required facts have separate tests.

The generic immutable-field cases pin the distinction between C++ default
construction and common immutable traversal: with explicit partial constructors,
list/set/map-value cases measure `hasDefaultConstructor == true` and
`needsAllFieldsConstructor == true`, whereas an immutable map key alone measures
true and false respectively. The default-sort records include stable orders,
actual reordering, aliases and generic children, constants, struct functions,
function exception error types, lambdas and filtered non-named inputs.
Raw generic children, self references, idempotence, duplicate rejection and
cycle diagnostics have native regressions; the oracle also constructs actual
JVM alias-cycle inputs directly to isolate sorter failures from loader behavior.

Five whole-model, comment-free fixtures render the unchanged production
`cpp/CppClass` or `cpp/CppStruct` and their transitive partials with both native
controls enabled and the **entire hooks object removed**. The class case really
moves a nested struct ahead of its alias and exercises sibling forward
declarations. The struct cases cover nested type collections, partial defaults,
immutable fields and C++ accessors with an explicit field constructor. Exact
JVM UTF-8 bytes, whitespace and final newlines match. Measured public getter
overlays and absent properties remain identified separately in the oracle
documentation. M8 fragments and all original 34 JVM fixture pairs retain their
existing comparison coverage.

Strict regressions cover mixed modes, replay hooks/catalog rejection, invalid
options, empty-input selector registration, unavailable context, nonempty text,
legal recursion, invalid cycles and existing output/stdout preservation. Raw
fact mutations demonstrate that native results do not depend on captured
answers or computed getter overlays. The release verification remains
formatting, offline Clippy with warnings denied, all Cargo tests, Python and
reference-model checks, JVM fixture reproduction, 315-template byte equality,
preview corpus and compiled C++ consumers. The final acceptance run passed 66
Rust tests, reproduced all 41 JVM fixture pairs and verified all 315 source
templates. Review fixes, verification commands and publication commits belong
to the linked evidence documents. These measurements establish this bounded
slice rather than whole-backend parity.

Work remaining after M9 included nonempty/native documentation, arbitrary
externals and name-rule files, complete attribute/view/helper coverage, canonical
frontend adaptation, complete headers/output sets and C++ runtime/ABI. M10 below
delivers headers/output sets for its guarded subset; broader P1b remains open.

### M10 / P1b.1: native C++ whole-file generation from snapshots — guarded subset delivered

The M10 plan/checklist was committed in `d1f31d095` before implementation,
from the verified M9 baseline `d2e69b620`. Delivered the native generator in
[`src/cpp_generation/mod.rs`](src/cpp_generation/mod.rs) and raw dependency
collectors in [`src/cpp_generation/collect.rs`](src/cpp_generation/collect.rs).
Initial collector and generator commits are `b116f2743` and `ea16f63f4`;
whole-file fixture and raw-mutation evidence extends through `6b1de0233`.
All changes remain under `ruscodium/`, all 315 production Mustache templates
remain unchanged, and the standalone `-generators cpp` preview stays separate.
Sol 6.1 max owns planning, Terra 6.1 xhigh implementation and evidence, and
Sol 6.1 xhigh independent review. The exact job/view contract is documented in
[GENERATION.md](GENERATION.md); final verification, review disposition and
publication are tracked in [TASKS.md](TASKS.md) and [REVIEW.md](REVIEW.md).

#### Native input and execution contract

The native CLI is:

```text
ruscodium generate-cpp --job FILE --templates DIR --output DIR
```

The library `cpp_generation::generate` returns all relative output paths,
`MAIN`/`COMMON` source sets and file contents in memory. Its separate
`write_files` step performs filesystem preflight and writes the inventory.
The command consumes a strict JSON job with
`schema: "gluecodium.cpp-generation-job"`, `version: 1`, `snapshot` containing
the full version-1 `LimeModel` reference graph, optional `property_overlays`
and `absent_properties`, and optional `options`. The permitted options are
`root_namespace`, `internal_namespace`, `export`, `export_common`, and
`copyright_header`. Namespace defaults are `[]`, export defaults to
`_GLUECODIUM_CPP`, common export defaults to the main export, and copyright
defaults to null, matching `GeneratorOptions`. Keys, types, ASCII C++ identifier
spellings and graph relationships are validated. A render request, selected
`data` root, caller-selected template, helper hooks, generator context or
precomputed output inventory is rejected. Native names, all eleven predicates
and the default sorter are mandatory, with no replay fallback or JVM subprocess.

Snapshots and measured getters remain a frozen frontend boundary. The snapshot
requires the full model root, main/auxiliary roots, reference map, builtin types
and enclosing declarations; the admitted stored fields and their typed edges
are validated. Output ownership comes from `topElements`; auxiliary roots are
available for lookup and own no output. Selected-object graphs and missing or
contradictory owners/references fail instead of acquiring invented context.

The measured getter allowlist is `name`/`fullName` on named elements,
`actualType` on types, `isEmpty` on comments, `isVoid` on return types,
`exception` on functions, `uniqueEnumerators` on enumerations,
`uninitializedFields` on structs, and `fields`/`struct` on field constructors.
Each getter value has a checked kind/class. Generation recomputes declaration
path names, void returns, uninitialized fields, unique enumerators and field
constructor membership/ownership from raw graph facts. Function exceptions must
be null, and the native providers resolve aliases from raw references.
Empty-comment evidence remains measured because snapshot fields omit private
comment text. Permitted absences are limited to verified lexical lookup fallback
names; the renderer supplies its own verified missing partial-local names.
The [oracle documentation](tools/cpp-generation-oracle/README.md) records their
provenance and complete lists. Generated includes, forward groups, dependencies,
sorted orders, resolved C++ names and predicate answers cannot be imported as
frontend views or stored generator contexts.

#### Supported C++ model and complete file sets

The guarded backend accepts comment-free ordinary classes/interfaces, structs,
enumerations, aliases and lambdas within the native type/name/control surface.
The [fixture matrix](GENERATION.md) proves synchronous nonthrowing methods,
read/write, read-only and static properties, field-bearing structs, literal
defaults, field constructors, nested declarations and cross-root references.
It includes numeric/string types, list/map/set fields, nullable values and
class/interface references. Literal and null values are admitted; other value
variants are rejected. The only admitted attribute is `@Cpp(Name)` with a
supported identifier. Existing native-provider limitations still apply to any
unimplemented type/name/value combination.

Preflight rejects nonempty/excluded/unavailable documentation, nonempty comment
placeholders, external descriptors, inheritance, exceptions/throws/error enums,
equality, async, filtering/tags, custom naming rules, unknown attributes/classes
and malformed type graphs. Repeated mapped method and property-accessor names
are also rejected until the upstream signature/overload validator is ported.
Validation covers the whole admitted graph, including auxiliary declarations.
User code supplies concrete implementations of abstract generated APIs. Generated
parameter documentation may still occur in files from comment-free LIME input.

For accepted jobs, generation follows upstream file ownership and template
selection: classes/interfaces, structs and enums have `.h` and `.cpp` files;
aliases and lambdas have headers. The unchanged `cpp/CppHeader` and
`cpp/CppImplementation` execute their transitive partials, including class
constructors/destructors and struct constructors. Empty-body enum implementation
files are retained. Every job also generates all eighteen common/export files:
thirteen common headers, three common implementations and the two export headers.
Unused helpers are included and rendered from the unchanged `cpp/common`
templates. The output preserves `MAIN`/`COMMON` identity and the upstream
`cpp/include` and `cpp/src` paths. Exact evidence covers complete C++ file sets
for the fixture subset; broader language-feature and runtime/ABI parity remain
open.

#### Native generator decisions

The collectors port the supported branches of `LimeTypeHelper`,
`CppImportsCollector`, `CppIncludeResolver`, `CppIncludesCache`, both C++ include
collectors and `CppForwardDeclarationsCollector`. They walk raw nested types,
type references/generic children and supported values, preserving alias and
owning-root include behavior, class/interface forward eligibility, nested-type
exclusions and namespace grouping. Include ordering is internal before system,
then filename, with deduplication, upstream self-header filtering and native
export/helper includes. Implementation includes use their own collector and
self-header. No dependency decision comes from scanning generated C++ text.

Paths follow `CppNameRules.getOutputFilePath`: root namespace, package path and
the owning outer type's default name or supported rename. Export filenames use
`Export`/`ExportCommon` plus upper camel export names. Namespace, export and
model/header/implementation data are assembled inside the generator. Its scoped
copyright resolver applies null or multiline custom contents to model/common
files with the exact template whitespace and final newlines; protocol/compiler
version metadata does not invent a generated banner. The inline-definition
whitespace fixes culminating in `682b44479` support genuine full headers while
retaining the earlier JVM template fixtures.

The generator renders every output and validates its relative path and model/
helper collisions before any write. Identifier/path guards reject separators,
absolute paths and parent traversal; the writer also preflights existing output
symlinks. Input/model/configuration/render/path preflight errors preserve existing
files and create no generated artifacts. Repeated jobs have deterministic
inventories/bytes and retain unrelated files. An I/O failure during the final
write loop may leave a partial update; filesystem transactions and concurrent
filesystem-change guarantees are outside this contract.

#### Oracle and completion evidence

The reproducible [whole-file oracle](tools/cpp-generation-oracle/README.md)
loads actual LIME and invokes the installed unchanged Kotlin
`CppGenerator.initialize`/`generate`. It exports the full raw graph and measured
views separately from expected files/source-set manifests; neither a captured
render context nor native-built template data supplies the expectation. The
oracle records compiler/template provenance, source grouping and options, and
runs each group in a fresh JVM because copyright initialization is process-wide.

The default and custom groups compare every relative path, `MAIN`/`COMMON`
identity and UTF-8 byte, including all helpers and empty-body implementations.
The default group exercises the root kinds, fields/defaults/field constructors,
properties, containers and genuinely dependency-reversed nested aliases. The
custom group adds nonempty root/internal namespaces, distinct exports, multiline
copyright, a renamed root, class forwards and nested-type includes. Its
auxiliary root is unreferenced: the fixture proves its indexed presence and
output exclusion, not referenced-auxiliary whole-file parity. Exact fixture
inventories and current comparison counts are maintained in
[GENERATION.md](GENERATION.md) and [TASKS.md](TASKS.md).

[`tests/cpp_generation.rs`](tests/cpp_generation.rs) proves raw type, name,
package-path and declaration-order mutations affect generated dependencies,
forwards, paths and bytes without changing getter overlays. Negative cases
cover forged context/replay input, invalid stored fields/typed edges, overlays,
reference maps, auxiliary cycles, unsupported content, paths/collisions and
output-sentinel preservation. Native outputs and the JVM captures compile all
their generated implementation files and run consumers with
`-std=c++17 -Wall -Wextra -Werror`, exercising generated value constructors and
concrete API implementations with the generated common runtime sources.

The acceptance checks retain formatting, offline Clippy/Cargo, Python and
reference-model tests, JVM template reproduction, all 315 unchanged templates,
the preview corpus and prior C++ consumers. Final aggregate commands/counts,
independent review and publication remain recorded in the linked task/review
documents. This delivers the guarded snapshot backend; canonical native
frontend adaptation, nonempty comments, overload/inheritance validation,
remaining C++ features/ABI and Dart/Swift/JNI/platform outputs remain open.

### M11 / P1b.2: smoke acceptance inventory and bounded native documentation — guarded subset delivered

The M11 plan/checklist was committed in `1b3151a81` from the clean `d9dc5b901`
baseline before implementation. The raw JVM documentation captures are in
`6d9e9808b`, the reproducible smoke baseline in `4e585e5e7`, and the native
implementation in `84377ae1e`, with final tooling/provenance through
`1dedc2ac8`. Sol 6.1 max planned this increment, Terra 6.1 xhigh implemented it,
and Sol 6.1 xhigh independently reviewed it.
All changes remain under `ruscodium/`, all 315 production templates remain
unchanged, and the standalone preview backend stays separate. The exact input
and formatter profile is documented in [DOCUMENTATION.md](DOCUMENTATION.md).
Final verification and review disposition belong to [TASKS.md](TASKS.md) and
[REVIEW.md](REVIEW.md).

#### Reproducible upstream smoke inventory

Delivered the [smoke runner and baseline](tools/cpp-smoke-matrix/README.md) for
thirteen complete upstream groups: `basic_types`, `enums`, `typedefs`, `lambdas`,
`properties`, `structs`, `nesting`, `comments`, `inheritance`, `async`,
`external_types`, `namespace_basic`, and `skip`. The report records exact
main/auxiliary sources and configuration hashes, effective C++ options, tags,
placeholders, JVM/compiler/template provenance and native revision. It uses the
real `OptionReader` for scenario overrides; otherwise it uses the smoke C++
internal namespace `gluecodium` and internal prefix `foobar_`.

Each fresh JVM process loads the original unfiltered model and independently
invokes the actual unchanged C++ generator. Export does not pre-apply JVM
filtering. General `Gluecodium.validateModel` is outside this generation
inventory. Captures compare fresh JVM results, rather than assuming checked-in
smoke files use default options. Native success requires the entire relative
path set and every byte, plus actual native library `MAIN`/`COMMON` source sets
checked through the inventory helper, including all eighteen common/export
files. Source sets are not inferred from the oracle manifest.

The version-1 baseline was produced with the executable from `d9dc5b901` before
native documentation changes. Reports distinguish exact matches, native
rejections, output mismatches, JVM failures and export/inventory errors; the
first observed guard is not a complete feature inventory. The configured tags
in `skip` remain an explicit unsupported native option rather than disappearing
at export. All selected groups remain represented. Current counts, measured
blockers and reproduction commands are maintained in the smoke README and
[TASKS.md](TASKS.md); guarded rejections never count as compatibility successes.

M11 additionally compares separately loaded, unmodified
`comments/input/CommentsInterface.lime` and
`comments/input/CommentsLambda.lime` with exact whole-file results. These focused
successes do not establish acceptance of the complete `comments` group. The
full-group acceptance boundary remains guarded; the inventory guides impact
ordering for subsequent feature work.

#### Explicit raw-documentation boundary

Generation job version 2 requires `raw_comments`, a complete map from every
`LimeComment` node ID, including empty and placeholder comments, to ordered
`[tag, text]` string pairs. The reference snapshot remains version 1; paths,
exclusion flags and placeholder-reference maps remain its stored graph facts.
The existing default/custom version-1 captures and default reference exporter
are unchanged. Version 1 rejects `raw_comments` and retains its measured-empty
contract. Version 2 rejects comment `isEmpty` overlays and never falls back to
that measured admission.

The [documentation oracle](tools/cpp-generation-oracle/README.md) uses a narrowly
scoped, checked reflective export of private `LimeComment.taggedSections`. It
records raw pairs with their profile/provenance, without changing production
Kotlin or importing `getFor`, serialized comment projections, formatted Doxygen,
resolved C++ names or predicate answers. Unknown/incomplete IDs, wrong classes,
malformed pairs and invalid placeholder references fail. This profile still
imports a JVM-loaded model; it does not supply a native LIME/Limedoc parser or
a complete canonical frontend adapter. Other allowed measured getter/absence
boundaries remain explicit in [GENERATION.md](GENERATION.md).

#### Native algorithms and conservative formatting

The native [comment module](src/template/native_comments.rs) derives raw
`isEmpty` from all section payloads across platforms. It selects universal,
exact `Cpp`, and `Placeholder` sections in order, recursively substitutes named
comments and applies the source trimming rules at each expansion. Template
views, comment name resolution and `hasAnyComment` use these native facts.
Global raw emptiness, selected text emptiness and selected text blankness remain
distinct: Java-only text can be globally nonempty and supply no C++ text.

Placeholder maps are checked, including unused edges, with explicit cycle,
depth and expansion-size guards and memoization for repeated references.
Configured loader placeholders use the supported one-level case; recursive
raw-graph tests are identified as synthetic model evidence. Native mutations
change text, platform selection, placeholder output, comment presence and
exclusion without refreshing captured answers.

The formatter implements a measured plain Unicode prose, paragraph and newline
profile of `CommentsProcessor`/`DoxygenCommentsProcessor`; it preserves admitted
soft line breaks without wrapping long lines. Admission is conservative even
for some punctuation that could be literal prose. [DOCUMENTATION.md](DOCUMENTATION.md)
defines the exact guards. Unsupported Markdown, documentation links and
unproved whitespace/control forms reject after platform selection and
placeholder expansion; ignored other-platform text does not determine the C++
formatter result. Full Flexmark formatting and scoped reference/name-map
resolution remain deferred, with no replay or JVM fallback.

The unchanged C++ documentation partials render raw exclusion, functions,
parameters, returns, properties, fields and struct/field-constructor comments.
Lambda `parameterName()` derives from the raw path. Legacy template requests
and version-1 generation preserve their previous behavior. `@Deprecated` and
other unsupported attributes, inheritance, filtering/tags, externals, errors and
other previously guarded C++ features remain rejected.

#### Bounded completion evidence

The fresh JVM oracle supplies all expected files and source-set manifests for
the two upstream-file units and a focused real-LIME fixture covering Unicode,
paragraphs, mixed/platform-only text, ordered concatenation, configured
placeholders, exclusion and member/constructor documentation. The complete
native outputs match those paths, source sets and bytes. Generated
implementations compile with strict C++17 flags and run their consumers;
repetition with the JVM unavailable preserves the expected output.

Negative and raw-mutation evidence covers raw-empty versus selected-empty/blank
text, empty placeholder expansion, malformed/incomplete maps, wrong IDs/pairs,
cycles, excess expansion, forged projections, expanded unsupported syntax and
auxiliary/late documentation failures. Preflight errors preserve empty stdout
and existing files. Final write-phase I/O retains the limitations documented in
[GENERATION.md](GENERATION.md).

Formatting, offline Clippy/Cargo, Python/reference-model checks, the existing
whole-file and template oracles, all 315 unchanged templates, preview corpus
and compiled consumers remain in the acceptance run. Exact final counts,
independent formatter probes, review findings/disposition and publication are
recorded in the linked task/review/oracle documents. This delivers a bounded
native documentation slice; full smoke, Markdown, native frontend, C++ feature/
runtime ABI and platform-backend parity remain open.

### M12 / P1c: native frontend adapter to the C++ compatibility backend — bounded subset delivered

Delivered the native LIME-to-C++ compatibility pipeline from baseline
`d1966f390`, following the committed M12 contract `a1a75760c`. Sol 6.1 max
planned the increment, Terra 6.1 xhigh implemented it, and Sol 6.1 xhigh
independently reviewed it. All changes remain under `ruscodium/`; the 315
production Mustache templates remain unchanged. The preview API/CLI and its
standalone C++ declaration generator remain separate interfaces.

Real LIME now passes through native loading, resolution and adaptation into
`cpp_generation` whole-file generation. This path requires no JVM, reference
export subprocess, captured job/model, imported getter answer, expected output
inventory or rendered context. It reconstructs the strict backend's graph and
views from native declarations. This delivers the bounded connection prioritized
by M12; the template-complete canonical contract and full Kotlin-model/frontend
parity in M6/P0/P3 remain open.

#### Delivered native model and adapter boundary

The public `cpp_adapter` module provides `build_job(&Model, &Options)` and
`generate(&Model, templates, &Options)`. Generation returns the existing
`GeneratedFile` records through `cpp_generation::generate`, then the CLI uses
`cpp_generation::write_files`. Caller-supplied backend snapshots, overlays,
absence maps, replay hooks, inventories or rendered contexts are not inputs to
the native compile interface. Internally constructed v2 jobs and getter views
are derived model facts, not captured JVM answers.

The adapter clones public models, guards schema/file/declaration/type/literal
shapes across main and auxiliary files, clears incoming resolved targets
recursively, and resolves references afresh. Per-kind fields, builtin identity
and arity, names/imports, raw versus structured annotation/literal consistency,
and otherwise unused or late declarations receive checks before rendering.
Unsupported facts reject rather than disappear. `Parser::typ` now retains
`TypeRef.docs`, with empty docs omitted from serialization so comment-free
preview JSON stays compatible. Unsupported type-local and recursively nested
metadata remains available for diagnostics instead of being discarded.

Deterministic allocation followed by linking constructs all seventeen basic
types, ordered main/auxiliary roots, reference and file-name maps, paths and
ownership, attributes/comments, ordered member collections, generic/nullable
references and aliases, methods/returns/parameters/accessors, defaults,
enumerators and field-constructor links. Names, child types, actual types,
implicit accessors/returns and admitted getter views are computed natively.
Generation retains the backend's strict shape, reference and ownership checks.
Admission follows source kinds and semantics, without fixture path/name/input
allowlists or expected-file lookup.

The demonstrated surface includes the original default/custom enums, aliases
and dependent-first nested aliases, named/positional lambdas, classes/interfaces,
structs and nested declarations, synchronous methods, omitted/explicit returns,
readonly/mutable/static properties, supported defaults, field constructors,
basic/container/nullable types and supported `@Cpp` names. Live JVM comparisons
also cover open/narrow declarations, constructors, static/struct methods,
additional numeric literals and name annotations on nested types and members.
The precise boundary and usage are in [FRONTEND_ADAPTER.md](FRONTEND_ADAPTER.md);
inheritance, exceptions/throws, external descriptors, filtering, arbitrary
attributes, unsupported overloads/literals and unimplemented source/model forms
remain guarded. A parser success alone does not admit a backend feature.

#### Separate native CLI and options

`ruscodium compile-cpp --input PATH [--input PATH] [--auxinput PATH]
--templates DIR --output DIR [--options FILE]` uses deterministic native input
discovery/deduplication. It requires main input, templates and an explicit output
directory; unknown flags, missing values and duplicate scalar options reject.
Repeated input/auxiliary flags are intentional. `--job` and model/context
injection are not accepted. Existing preview commands and `generate-cpp --job`
retain their distinct contracts.

The strict `gluecodium.native-cpp-options` version-1 JSON contains only
schema/version and five backend settings: `root_namespace`,
`internal_namespace`, `export`, `export_common` and `copyright_header`.
Defaults are empty namespace arrays, `_GLUECODIUM_CPP`, inherited common export
and null copyright. Namespace components and export identifiers are checked;
copyright preserves supplied newlines. Invalid types, unknown fields, unsafe
identifiers and unsupported schema/versions reject before writing. The options
cannot supply graph data or precomputed generator decisions.

Adaptation and every model/common/export render finish in memory before output
writes. Input, configuration, model and template failures produce nonzero status,
empty stdout and preserved output inventories/sentinels. The final write phase
retains the I/O limitations and unrelated-file behavior documented in
[GENERATION.md](GENERATION.md); filesystem transactionality is not claimed.

#### Bounded native source documentation

Native line-comment parsing now maps admitted plain `//` text, paragraphs,
platform sections, exclusion and supported parameter/return/property/constructor
blocks into M11's v2 raw-comment contract. Every real or synthetic comment node
has a native raw-section entry; genuine emptiness is derived after source facts
are checked. Comment paths, source section order, tags and exclusion are retained
for the existing formatter rather than supplied as formatted text or legacy
`isEmpty` answers. Actual JVM ownership semantics are preserved for ordinary
property comments, named parameter blocks and synthetic field-constructor
parameter comments derived from fields.

The two unmodified upstream interface/lambda documentation files are admitted
as separately loaded acceptance units. This does not admit the complete
comments smoke group. Block comments, placeholders, type-position docs,
directly attached parameter/accessor/return-type docs, explicit `@param` blocks
on field constructors, unsupported tags and full Markdown/reference processing
remain explicit errors. The options profile has no placeholder configuration;
the focused M11 placeholder job remains backend regression evidence. These are
concrete documentation blockers, not an assertion that user comments are empty.
See [DOCUMENTATION.md](DOCUMENTATION.md) and the adapter boundary for details.

#### Acceptance evidence and limits

The mandatory first gate passes on real native LIME: all 26 default and 24
custom relative paths, actual `MAIN`/`COMMON` source sets and every byte match
independently loaded JVM models and the original captures. Each job includes
all eighteen common/export files. The custom auxiliary root participates in
lookup without owning output. The two isolated upstream documentation inputs
add 20 files each, for 90 baseline files across four jobs.

The [frontend adapter oracle](tools/frontend-adapter-oracle/README.md) compares
an explicit semantic projection of independently loaded native/JVM models.
It preserves ordered roots/members, kinds, paths/owners, attributes, direct and
resolved type/generic/alias/nullability edges, parameters/returns/accessors,
static/constructor facts, defaults, enumerators, constructor links, comments,
reference membership, builtins and file ownership by unambiguous basename.
It normalizes traversal IDs,
allocation artifacts, equivalent getter views and physical source prefixes;
unknown classes/fields or inconsistent targets fail. The oracle documents the
complete coverage and exclusions. This is bounded semantic evidence, not full
canonical-model equivalence.

Both library output and CLI output from a temporary working directory with
empty `PATH` and unset `JAVA_HOME` reproduce the baseline inventories/bytes.
All baseline model/common implementations and the existing consumers compile
with `-std=c++17 -Wall -Wextra -Werror` and run. Deterministic repetition and
independent negative CLI/model probes cover forged mutable models, stale targets,
unsupported auxiliary/late facts, invalid configuration, collisions and render
failures with preserved pre-write output.

Live raw-LIME mutations compare complete output and semantic projections to
fresh JVM loads for names/packages, dependency order, references/nullability,
values, auxiliary lookup/ownership, measured declaration/name forms and bounded
documentation. Mutation evidence establishes byte/model compatibility; it does
not establish compilation for every mutation. In particular, integer separators
retain the JVM spelling `1_000`, which is invalid C++. Compiled-consumer claims
apply to the baseline jobs, not that numeric form.

The final acceptance run passed formatting, offline all-target Clippy/Cargo,
Python/reference-model checks, retained fifty-file whole-generation and 63-file
documentation oracles, all 41 template request/output pairs, direct equality of
all 315 production templates, preview corpus and compiled consumers. Final commands/counts,
reviewed candidate hashes, findings/disposition and publication status are
recorded in [TASKS.md](TASKS.md), [REVIEW.md](REVIEW.md), the
[frontend oracle](tools/frontend-adapter-oracle/README.md) and retained
[backend oracle](tools/cpp-generation-oracle/README.md).

This milestone delivers the native frontend adapter and bounded source
comments for the measured C++ compatibility subset. Full canonical/Kotlin-model
parity, complete validation/documentation, all-feature C++ runtime/ABI parity and
Dart/Swift/JNI/platform outputs remain open.

### M13: reproducible Kotlin/JVM versus Rust performance comparison — bounded measurement delivered

The contract was committed in `141fe1cd5` before benchmark implementation.
Sol 6.1 max planned this milestone, Terra 6.1 xhigh implemented the experiment,
and Sol 6.1 xhigh independently reviewed its corrected evidence. The delivered
[performance report](PERFORMANCE.md), [reproduction README](tools/performance/README.md)
and [independent review](REVIEW.md#m13-independent-performance-review--2026-11-01)
record the final methods, results and limitations. All additions stay under
`ruscodium/` on `ruscodium/rust-port`; production compiler behavior and all
315 production templates remain unchanged. This milestone measures the M12
subset and implements no production optimization.

#### Actual compiler boundary and source identity

The primary experiment measures fresh processes from launch through exit after
complete C++ output writes. The JVM side invokes installed Gluecodium 14.2.2's
actual `com.here.gluecodium.Gluecodium` main directly with `-generators cpp`,
caching disabled and its normal full load/validation/generation path. The Rust
side invokes the rebuilt optimized native `ruscodium compile-cpp` command.
Both receive the same raw LIME and equivalent namespace/export/copyright
settings and write complete output trees to fresh separate destinations on the
same filesystem. Neither timing path consumes a reference-model export,
captured graph, preview declaration generator or pre-parsed input. Builds,
fixture preparation and complete output verification occur outside timers.

The release binary was built with `cargo build --offline --release` from
`141fe1cd5`, whose production sources equal `12e45a188`; the intervening commit
only added this milestone's plan. Corrected run manifests identify clean
benchmark source `311528689`, and the final results/report are committed in
`e8eca0c31`. Independent review is committed in `7462775b8`. Raw records pin
the native binary, JVM runtime/application/dependency jars, helper sources,
input/options and template hashes; review checked those identities against
the actual artifacts. The report records toolchain and environment details
without assuming that the installed JVM distribution equals repository HEAD.

#### Valid inputs, parity and scaling

The completed matrix includes the real custom fixture with auxiliary lookup
and custom options, a copied default fixture and deterministic independent
one-field-struct workloads at 10, 100 and 125 structs. The default benchmark
copy changes `field constructor(label)` to
`field constructor(label, mapping, tags)` so the actual JVM validators accept
its required nondefault fields; the original fixture is unchanged. Both
frontends receive and validate each workload. Controlled struct scales probe
this admitted surface rather than represent complete application projects.

Every completed workload passed a pilot gate comparing full relative file
inventories and exact bytes, including common/export files. Every formal
sample, filesystem warmup and persistent iteration was independently checked
against its complete baseline outside the timer. Per-file and aggregate hashes,
source/output sizes and precise counts are retained in the linked report and
raw [pilot](tools/performance/results/pilot.json),
[fresh-process](tools/performance/results/fresh.json) and
[persistent-process](tools/performance/results/warm.json) records. Independent
review rehashed the actual generated output trees and found no mismatch.

The 500-struct pilot succeeded on the JVM but the native process was killed at
its predeclared 60-second limit without completed output parity. Its censored
record remains visible and has no parity or speed-ratio claim. The 125-struct
fallback was defined before the pilot and admitted after that timeout. Slower
native results at both 100 and 125 structs remain in the completed matrix.
No favorable timing result was used as an input-selection gate.

#### Sampling and corrected measurement evidence

Fresh-process trials use warm filesystem caches, separate JVMs, a saved seeded
balanced/interleaved schedule and sequential paired invocations. Each completed
workload has eight pairs. A small native C supervisor measures monotonic wall
time, per-child user/system CPU and Linux per-process peak RSS through blocking
`wait4`, avoiding Python polling delay and Python-parent RSS contamination.
The report gives medians, interpolated quartiles, ranges and the JVM/Rust median
wall-time ratio with actual times and memory values. Shared-host contention,
a two-CPU cgroup quota, an 8 GiB memory limit and buffered tmpfs output remain
explicit limits; filesystem warmup is neither warmed JVM JIT nor a controlled
OS-cache-cold experiment.

An initial logging configuration could not write the JVM home and emitted
exception traces. The complete experiment was rerun with a pre-created writable
`-Duser.home`; logger initialization failures now invalidate invocations.
Historical diagnostics and preliminary measurements remain under
[initial-logging-error](tools/performance/results/initial-logging-error/) and
are excluded from final statistics. The corrected evidence is log-clean.
Independent review also verified timeout/exit handling, source identities,
complete-output parity and every reported statistic and ratio.

A separate persistent API experiment repeats full load, validation, generation
and writing for the 10-struct workload after explicit warmup. Options are parsed
outside iteration timers and outputs have fresh destinations. It measures wall
time only, uses one process per implementation and has correlated iterations;
it does not establish JIT steady state or per-iteration CPU/RSS. Larger cases
were excluded by the declared pilot budget. Its results remain separate from
the fresh CLI comparison.

#### Delivered conclusions and remaining work

Fresh native processes are faster on the two real fixtures and 10 structs;
the JVM is faster at 100 and 125 structs and in the small persistent experiment.
Native peak RSS is lower on every completed fresh workload. The report links
the exact measured values, raw samples, commands and reproduction steps.
Visible repeated whole-graph import and class-wide absence scans during native
file rendering support a scaling hypothesis; no profile establishes a
bottleneck and no optimization was implemented in this milestone.

Independent review reports no unresolved material finding within the M13
measurement contract. Equal generated bytes for these inputs do not equate
the guarded native frontend's validation obligations with the broader JVM
validators, establish statistical significance, isolate language overhead or
claim full compiler compatibility. Complete canonical/frontend validation,
all-feature C++ and platform parity, further performance work and migration/
cutover policy remain open in the roadmap below.

### M14: remove repeated generation preparation — bounded optimization delivered

The user requested optimization after M13 measured native medians of 21.018
seconds for 100 structs and 33.096 seconds for 125 structs, with the native
500-struct pilot reaching its 60-second limit. The optimization baseline is
`15b1db4c4` on `ruscodium/rust-port`. The contract and checklist were committed
before implementation in `965a9ed96`; implementation is `6ccea17bc`, with
additional prepared-renderer regressions in `ec381af93`. Sol 6.1 max planned,
Terra 6.1 xhigh implemented and Sol 6.1 xhigh independently reviewed the
bounded milestone. All changes stay under `ruscodium/`, all 315 production
templates are unchanged, and M13's report, charts and raw results remain intact
as historical evidence. The new [optimization report](OPTIMIZATION.md),
[raw comparison](tools/performance/optimization-results/optimization.json) and
[operation counts](tools/performance/optimization-results/counts.json) record
the measured behavior and its limits separately.

#### Measured repeated work and delivered changes

Separate baseline instrumentation in `8888fb09c` confirmed repeated preparation:
10 structs produced 39 graph imports, 58 native resolver constructions, 204
file-partial parses and 8,089,290 graph-import absence-node probes; 100 structs
produced 219 imports, 418 resolvers, 1,734 parses and 2,183,649,930 such probes.
Both diagnostic output trees matched M13's complete JVM inventories. The
retained script and count records identify the original source, insertion
sites, executable and commands. Successful imports have no early conflict
return, permitting the counted `node count × absent-name count` probe total.
These counts cover graph-import absence validation only and provide no sampled
time attribution or bottleneck percentage. The diagnostic binary was excluded
from timings.

The implementation preserves the admitted feature set and changes four paths:

1. A generation-scoped prepared renderer owns the validated rendering graph,
   raw comments and native resolver. Fresh file engines borrow that read-only
   state instead of building graph-sized JSON requests and reimporting them.
   Original-job validation and derived-overlay preparation retain their order;
   the original-model graph remains distinct from the final rendering graph.
   A shared dependency-collection context reuses its path index and native
   resolver across generated declarations. Preparation is lazy to preserve
   existing error boundaries.
2. Class-to-property-name unions replace repeated all-node absence scans in
   graph import, native adaptation and derived generation absences. The importer
   builds its union after overlays, preserving exact-class conflicts, stored
   null getters, node-specific absences, unknown IDs and duplicate-name rejection.
   Reference validation uses the current graph node map, so public node-map
   mutations do not produce a stale ID cache.
3. File-partial syntax is loaded lazily and cached within a generation. Dynamic
   inline definitions retain precedence over cached disk partials and are
   collected on every encounter, preserving forward references and replacement
   semantics. Each output has fresh definitions, frames/locals, iteration
   metadata, switch state and recursion/output accounting. Independent calls
   and prepared renderers have separate caches and observe changed roots/files;
   no rendered bytes or request data are cached.
4. File syntax trees use shared immutable `Rc` ownership and engines borrow
   graph/resolver state. Dynamic definition bodies still clone when registered;
   this milestone does not replace every runtime value or AST allocation.
   Standalone request schemas, hook restrictions, generation job versions,
   validators and the supported subset remain intact. The prepared path is
   internal and follows the existing validation responsibilities.

#### Regression and compatibility acceptance

Three prepared-renderer unit tests compare shared-cache renders with fresh
standalone renders and cover per-file locals/definitions, inline-over-file
shadowing, replacement, forward/nested definitions, repeated partial encounters,
changed files, different roots/copyright settings, iteration and switch state.
An added graph regression covers a same-class overlay-null getter conflict,
different-class independence and live node-map mutation; existing rejection,
whitespace, recursion/output and symlink/path tests remain in force. Tests use
behavioral assertions rather than wall-time thresholds.

The 102-test Rust suite passed on the initial implementation, followed by all
three prepared-renderer tests after the two additional tests in `ec381af93`.
Final formatting and offline all-target Clippy with warnings denied passed.
Independent checks reran the template oracle's 41 JVM pairs and 315-template
identity gate, retained whole-file/documentation goldens and the native frontend
adapter oracle, including four baseline native jobs, semantic model projections,
23 live mutations, deterministic results, strict C++ consumers and output
preservation on rejected inputs. Generation still completes in memory before
writes. These cases establish bounded regression/output evidence; complete
C++ and frontend parity remain open.

The [independent review](REVIEW.md#m14-independent-optimization-review--2026-11-02)
in `cbd13c4b0` reports no unresolved material finding. It also passes 47 focused
integration tests, the three final prepared tests, eighteen adversarial CLI
probes and four harness checks. The CLI probes include malformed absences and
same-class cross-node stored null/string/false getters. Review independently
rehashes all 117 successful output trees and 28,786 files, and recomputes all
306 scalar statistics and eleven ratios against the displayed report tables.

#### Bounded before/after measurement

The rebuilt baseline `15b1db4c4` and optimized release at clean source
`ec381af93` ran in the same environment alongside the actual JVM compiler.
Tools are committed through `c2093ba80`, `a71c41f66` and `3f90a57a0`; report/raw
evidence is `412913187`, with counter-reproduction documentation in `67d16764b`.
M13's custom fixture, corrected default copy and independent one-field structs
at 10/100/125/500 use the same explicit options and unchanged templates. Timing
covers fresh raw-LIME `compile-cpp` through complete writes. Builds, fixture
preparation, logging setup, diagnostics and output hashing stay outside timers.
The retained records pin binaries, source/dirty state, jars, toolchains,
environment, argv, inputs/options/templates and complete output inventories;
identities matched again at completion.

The predeclared seeded schedule contains three baseline Rust trials per first
five workloads, eight balanced optimized-Rust/JVM pairs per all six, and one
baseline 500-struct attempt. All 112 attempts are retained with the same
60-second cap; 111 completed and matched complete reference inventories,
including common/export files. Six separate successful JVM equivalence
preflights are excluded from sample statistics. The one baseline 500 attempt
was killed at 60.009 seconds without an output tree and has no completed parity
or numeric baseline/optimized ratio. Output checks occur outside timers.

Same-host baseline/optimized median wall time fell from 20.844/0.089 seconds
at 100 structs (234.7×) and 44.499/0.157 seconds at 125 structs (283.2×).
Optimized 500 structs completed in median 1.296 seconds versus JVM 2.776
seconds, with all eight outputs per side passing the gate. Custom, corrected
default and ten structs also improved, with medians and CPU/RSS distributions
visible in the report. The earlier M13 125-struct median remains 33.096
seconds; it is historical evidence, not the denominator of this same-host
before/after comparison.

The results meet the bounded performance objective. Shared-host variation,
a two-CPU quota, an 8 GiB memory limit, buffered tmpfs writes, synthetic scales,
three-versus-eight native sample counts and broader JVM validation remain
explicit limits. These few scales do not establish asymptotic complexity,
statistical significance or language/runtime overhead. Fresh filesystem-warm
processes retain no JVM JIT state; M13's persistent API experiment remains
separate and no new warmed-API improvement is claimed. Broader compatibility
and further optimization remain open in the roadmap. The reviewed M14 commits
were pushed through `347792270` to `origin/ruscodium/rust-port`; the remote tip
was verified within the user's existing publication authorization.

### M15 / P1c.1: enum-backed synchronous exceptions and throws — bounded subset delivered

The increment from `0dc5def39` widens the actual native LIME-to-C++ pipeline
through one bounded runtime feature: exceptions with direct enum payloads and
synchronous throwing methods. Sol 6.1 max plans, Terra 6.1 xhigh implements,
and Sol 6.1 xhigh independently reviews the increment. The contract and checklist
were recorded in `9caabcc88` and clarified in `01d0f1223`.
All changes stay under `ruscodium/` on
`ruscodium/rust-port`; retain all 315 production templates unchanged.

This is compiler capability work after the delivered M14 optimization. The
M11 inventory reports `LimeException` as the first guard in six of twelve
rejected complete C++ smoke groups, but a first guard can mask unrelated gaps.
The native collector, predicates, naming and unchanged C++ return/category
templates already contain parts of this feature. At the baseline the adapter
and strict graph boundary rejected it, and generation supplied an empty `errorEnums`
list. Complete the connected feature with live compatibility and executable
runtime evidence; do not claim whole smoke groups or the calculator example
become supported merely because their exception guard moves.

#### Admitted native source and model facts

Admit top-level exceptions and exceptions nested in otherwise supported
classes, interfaces or structs. The exception payload must resolve **directly**
to a nonnullable, nonexternal enumeration within the existing enum subset.
Aliases to enums, scalar/struct/collection payloads, external payloads and
unsupported metadata remain explicit errors. A throwing method must resolve
its nonnullable throws reference directly to one of those exceptions. Aliases
to exceptions remain rejected. Existing enum/alias uses outside these new
positions retain their current contracts. The existing bounded safe
`@Cpp("Name")` profile may also annotate exception declarations, with fresh JVM
proof of the model/no-output behavior; this adds no annotation family or
exception output file.

Admit throws only on ordinary synchronous instance/static functions in the
existing class/interface/struct subset, with omitted/explicit `Void` or an
otherwise supported value return type. Throwing constructors, property
accessors and lambdas remain guarded, as do async functions, inheritance,
filtering and unrelated annotations. Preserve already admitted ordinary
documentation on declarations; this increment adds no documentation syntax,
throws blocks, directly attached throws/type comments or reference processing.
Any unimplemented source metadata must still reject before writes.

Construct native `LimeException.errorType`, ordered exception membership,
child types, reference/file ownership, `LimeThrownType.typeRef` and its genuinely
empty comment. Compute `LimeFunction.exception` from the thrown reference and
compute the new type/getter views natively. Caller-supplied resolved-target
caches, exception getters, rendered contexts, error-enum lists and generated
inventories cannot substitute for those source/model facts. Validate public
models across main and auxiliary inputs, clear relevant resolution caches and
resolve afresh just as M12 does for the existing subset.

Extend both original snapshot shape/value validation and semantic graph
validation for these classes and edges. Keep nullability, canonical indexed
targets, parent membership, ownership, payload kind and throw placement
consistent. Validate supplied getter overlays against their derivation rather
than accepting any exception with the right class or silently replacing a
contradictory getter. Apply equivalent rules to the computed rendering views;
stored fields, overlays and same-class/null getter variants must not bypass
the boundary. Extend the enumerated model projection to compare exception
payloads, thrown references/comments and the derived exception target.

#### Exact C++ behavior and ownership

Use the unchanged templates to emit `std::error_code` for enum-backed throwing
`Void` methods and the configured internal `Return<T, std::error_code>` for
value-returning methods. Reproduce header/implementation includes and their
ordering, declarations, error-category functions, error-code enum traits,
category names/messages and final whitespace byte for byte. Existing common
and export files and their source sets remain part of every comparison.

Match the JVM's discovery boundary: traverse **main** top-level elements and
their nested types to collect direct enum payloads of declared exceptions,
including unused exceptions. Auxiliary exceptions do not independently mark
enums as error enums. A main exception may reference an auxiliary enum, but
auxiliary ownership does not create an output file or a category implementation.
For each emitted owning root, select its marked nested enums in the JVM's
type-traversal order and deduplicate shared enum payloads. Cross-root declaration
order or throws usage must not accidentally control whether a main enum gets
its category machinery.

Top-level exception declarations retain model identity, membership and source
ownership while producing zero declaration/implementation files. Nested
exceptions similarly add no invented C++ declaration. They do not reserve
output paths or introduce collisions with a real emitted root whose C++ name
matches. Preserve the existing collision checks for actual generated files;
do not introduce broader file grouping or change unrelated name rules.

#### Acceptance and failure evidence

Add a focused fixture family to the native adapter oracle using fresh JVM
loads of the same raw LIME and options. Compare complete output paths, actual
`MAIN`/`COMMON` source sets and exact bytes, plus the explicit semantic model
projection. At minimum cover top-level and nested exceptions, direct enums
inside another owning root, multiple exceptions sharing an enum, an unused
exception that still marks its enum, multiple marked enums with observable
ordering, `Void` and value returns, instance/static functions, auxiliary lookup
and ownership, and a no-output exception whose default C++ name collides with
an emitted root. Live source mutations must change enum/package/member names,
enum values or throw targets and be rechecked against a fresh JVM result.
Expected captures may be retained for regressions but are never native inputs.

Compile and run native library and CLI outputs with
`-std=c++17 -Wall -Wextra -Werror`. A consumer must use generated enum-to-error
conversion, compare error categories and messages, implement and call admitted
throwing methods, and exercise success/error states of `Return`. Exercise
custom root/internal namespaces as well as defaults. Run the actual CLI with
empty `PATH` and no `JAVA_HOME` from a temporary directory to retain the native
execution proof.

Retain negative probes for payload aliases/non-enums/nullability, non-exception
or nullable throws, aliases to exceptions, throwing constructors and unsupported
metadata. Cover forged public-model caches and malformed snapshot/overlay
links, including inconsistent derived exception targets. Library errors and
CLI failures must precede all writes, leave stdout empty where required and
preserve pre-existing output trees/sentinels. Do not silently ignore a rejected
exception merely because it would own no generated file.

Pass formatting, offline all-target Clippy with warnings denied, Rust tests,
the extended projection/tool checks, existing adapter and C++ goldens/consumers,
the 41 template oracle pairs and the unchanged 315-template checks. Broader
smoke inventory may be rerun as a separate comparative report with new first
guards and full provenance; its acceptance counts must not replace the focused
feature evidence. Update `FRONTEND_ADAPTER.md`, generation/oracle documentation,
tasks and independent review with the measured boundary and any residual
limitations. Existing M13/M14 performance results remain historical evidence;
this milestone requires no new performance claim or platform backend work.

#### Delivered evidence and remaining limits

Implementation `3d07f3232` connects the native adapter, strict graph validation,
main-only error-enum discovery and unchanged templates. The live oracle in
`b27701d3b` compares eight fresh JVM cases: baseline and three source mutations
at 26 files each, class/struct owners at 30, exception-only input at 18, and
actual default/custom options at 22 each. All 196 paths, actual source sets,
file bytes and explicit model projections match. Twelve strict C++17 consumer
builds/runs cover JVM, library and Java-free CLI output for four cases. The
recorded [evidence](tools/enum-errors-oracle/evidence.json) pins source/tool,
input/options, binary, JVM and template identities plus complete file hashes.

All 106 Rust tests, formatting, offline all-target Clippy with warnings denied,
14 projection tests and four existing Python tool tests pass. Retained live
checks pass 90 native-adapter baseline files and 23 source mutations, 50
whole-file and 63 documentation captures with their consumers, all 41 template
pairs and all 315 unchanged production templates.

Independent Sol 6.1 xhigh review `f518651d6` reports no unresolved material
finding within this scope. It independently reproduces the final focused
oracle, verifies all 196 recorded output hashes, and adds 40 rejected CLI
probes preserving complete existing outputs, two positive job-compatibility
checks, four fresh JVM cases totaling 84 files and public-model cache mutation
checks. The exact coverage and disposition are recorded in [REVIEW.md](REVIEW.md).

The separate comparative smoke report in `77bdee61e` retains one exact complete
group and twelve guarded complete-group rejections, plus two exact isolated
documentation files (64 accepted files). All fifteen input/options/JVM
inventories and recorded environment identities match M11. Six first guards
advance to `DART`, three constant-value cases, Markdown and `ASYNC`; no row has
an output mismatch or provenance/JVM/export failure. These changes do not
establish additional whole-group parity. Aliased or non-enum payloads,
throwing constructors/accessors/lambdas, async, full documentation processing,
remaining model/attribute/value forms and other target backends remain open.
M13/M14 measurements and the original templates remain unchanged.

### P1b: complete JSON-consuming C++ compatibility backend — remaining work

Extend M10's snapshot-driven C++ generation and M11's bounded documentation
profile alongside M12's delivered bounded native adapter toward complete
canonical model and frontend coverage. Broaden that native path without making
full backend coverage a prerequisite for each bounded increment. Use the
template-surface report to implement typed property views and helper contracts
rather than assuming `serde_json` lookup reproduces Kotlin reflection. Extend
the native resolver through the remaining name,
Markdown/documentation-reference, external-descriptor and configurable-name-rule
contracts, and extend M9's predicates/sorter beyond the bounded imported model
and M11 comment profile.

Build on P1a's measured custom runtime and extend the explicit property/helper
contracts through the C++ backend. Template conversion is outside the chosen
approach. Preserve standalone tags, missing/null values, section context, helper
scope, indentation from `prefixPartial`, and final newlines as coverage grows.
The acceptance criterion is byte-for-byte compatibility on existing smoke
outputs, including whitespace; normalizing generated source or merely compiling
it is insufficient. Selected-template equality from P1a, native naming from M8
and native C++ predicate/sorter fragments from M9 do not satisfy this whole-backend
criterion. M10 supplies complete file-set comparisons for its guarded snapshot
fixtures, M11 adds exact plain-documentation cases, and M12 joins real native
LIME to that guarded backend. A complete canonical adapter, all-feature C++
generation, full Markdown/reference processing and remaining model/helper
coverage remain pending until verified.

Run both generators on the same canonical inputs and options, compare output
file sets and exact bytes, and expand coverage through all C++ smoke fixtures.
Keep this compatibility backend visibly distinct from the preview's standalone
C++17 declaration contract until the C++ runtime and output goldens agree.

### P2: bindings and platform backends — deferred

Port shared conversion, ownership and runtime helpers, then follow dependency
order: FFI before Dart, CBridge before Swift, and JNI before Java/Kotlin. For
each pair, first generate from canonical JSON and compare all file bytes against
the corresponding smoke goldens; then run existing platform functional tests.
Include configurable naming, filtering/tags, shared/internal source sets and
runtime lifetime behavior. Source-file similarity alone does not establish
bridge ABI or ownership compatibility.

### P3: frontend convergence and tooling — deferred

Extend M12's bounded native/JVM model comparisons and pipeline toward the
template-complete canonical contract and Kotlin-export goldens. Complete
all remaining model semantics, validators, Limedoc behavior and attribute rules.
The frontend built for the preview supplies a starting point without being
declared equivalent in advance. Compare negative diagnostics as well as valid
models, then broaden the proven native pipeline to every supported backend.

Complete options files/configuration, every supported CLI flag, static generator
selection, `Skip`/`EnableIf`, output caching and stale-file removal, split outputs,
and build-system integration. Only the resulting full matrix supports a
drop-in replacement claim.

## Roadmap to full Gluecodium compatibility

| Stage | Work remaining after the preview | Required evidence |
| --- | --- | --- |
| Canonical boundary | Extend the bounded snapshot/importer and M12 native adapter to a template-complete canonical schema and full Kotlin-model parity | Golden snapshots for coherent fixtures and completeness/schema/adapter tests |
| Template compatibility | Extend P1a's custom Rust runtime, property views and helper contracts while preserving original Mustache templates | Template inventory plus byte-exact helper/whitespace and smoke comparisons |
| C++ parity | Extend M10's guarded constructors/accessors/constants and common-helper output through every C++ attribute, name-rule files, equality, external types, `Return`, error categories and full API/runtime behavior | Existing C++ golden outputs and functional C++ tests |
| Runtime and binding core | Common conversion/runtime model, name resolvers, ownership, cache and lifetime contracts | Native conversion and lifetime regression tests |
| Dart | FFI then Dart source, finalizers, async and ownership semantics | Existing Dart smoke outputs and functional tests |
| Apple | CBridge then Swift source, nullable/external/generic/ownership behavior | Existing Swift smoke outputs and platform functional tests |
| Android | JNI then Java/Kotlin source, platform annotations, async decorators, parcelable behavior | Existing Android smoke outputs and functional tests |
| Frontend fidelity | Complete all Kotlin validators, filtering/tags, full attribute semantics, Limedoc references/placeholders, warnings/strict mode | Canonical-model comparisons and differential diagnostic cases from existing unit tests |
| Tooling compatibility | Options files, all CLI options, caching/stale-file handling, split outputs, CMake/Gradle integration and distribution | Existing launcher/build integration tests and packaging checks |
| Cutover | Define compatibility guarantees, publish migration guide, performance measurement and release policy | Full supported-platform parity matrix before replacing the JVM tool |

Preserve the preview's stable public boundaries where practical, but avoid
declaring its JSON schema or C++ ABI final before the corresponding parity work.
