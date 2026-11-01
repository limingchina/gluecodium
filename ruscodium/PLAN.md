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
in Rust. A template-complete canonical schema, an adapter from the preview
model, and JSON-consuming compatibility generators remain planned work;
neither existing emitter delivers that complete boundary by itself.

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
slice, M8 a bounded native C++ name resolver, and M9 native C++ predicates and
declaration sorting. The complete canonical boundary and subsequent backend
phases remain incomplete until their own acceptance evidence exists.

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
open within this experimental runtime. The native frontend-to-canonical
adapter, remaining native C++ helper implementations and whole-file compatibility
backend remain pending in the following phases.

### M8 / P1a.1: strict native C++ naming — bounded implementation delivered

Delivered a separate Rust name resolver over the imported identity graph in
[`src/template/native_cpp.rs`](src/template/native_cpp.rs), with JVM-generated
fixtures in commit `931251088` and native implementation in `5d9828539`.
It computes a measured subset of C++ names without recorded name results and
keeps all 315 production Mustache templates unchanged. This continues P1a; P1b,
the canonical frontend adapter and whole-C++ output/runtime parity remain open.

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

Nonempty comment processing, external descriptors, custom naming files and
complex defaults remain deferred. A measured empty comment resolves to the empty
string from its actual `isEmpty` fact; a missing comment fact is unsupported.
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
processing remain deferred.

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

Remaining work includes nonempty/native documentation, arbitrary externals and
name-rule files, complete attribute/view/helper coverage, canonical frontend
adaptation, complete headers/output sets and C++ runtime/ABI. M9's exact native
fragments narrow the replay boundary; they do not complete P1b or full parity.

### P1b: JSON-consuming C++ compatibility backend — deferred

Implement C++ generation from the canonical snapshots before tying it to Rust
frontend fidelity. Use the template-surface report to implement typed property
views and helper contracts rather than assuming `serde_json` lookup reproduces
Kotlin reflection. Extend M8's native resolver through the remaining name,
comment, external-descriptor and configurable-name-rule contracts, and extend
M9's predicates/sorter beyond the bounded imported model and comment facts.

Build on P1a's measured custom runtime and extend the explicit property/helper
contracts through the C++ backend. Template conversion is outside the chosen
approach. Preserve standalone tags, missing/null values, section context, helper
scope, indentation from `prefixPartial`, and final newlines as coverage grows.
The acceptance criterion is byte-for-byte compatibility on existing smoke
outputs, including whitespace; normalizing generated source or merely compiling
it is insufficient. Selected-template equality from P1a, native naming from M8
and native C++ predicate/sorter fragments from M9 do not satisfy this whole-backend
criterion. A complete canonical adapter, full C++ file generation, native
comments and remaining model/helper coverage remain pending.

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

After backend comparisons isolate generation behavior, compare the native
frontend's adapted canonical models against the Kotlin-export goldens. Complete
all remaining model semantics, validators, Limedoc behavior and attribute rules.
The frontend built for the preview supplies a starting point without being
declared equivalent in advance. Compare negative diagnostics as well as valid
models, then join the proven frontend and backends into one native pipeline.

Complete options files/configuration, every supported CLI flag, static generator
selection, `Skip`/`EnableIf`, output caching and stale-file removal, split outputs,
and build-system integration. Only the resulting full matrix supports a
drop-in replacement claim.

## Roadmap to full Gluecodium compatibility

| Stage | Work remaining after the preview | Required evidence |
| --- | --- | --- |
| Canonical boundary | Extend the bounded snapshot/importer to a template-complete canonical schema and implement the native frontend adapter | Golden snapshots for coherent fixtures and completeness/schema/adapter tests |
| Template compatibility | Extend P1a's custom Rust runtime, property views and helper contracts while preserving original Mustache templates | Template inventory plus byte-exact helper/whitespace and smoke comparisons |
| C++ parity | Name-rule files, every C++ attribute, constructors/accessors/equality, constants, external types, `Return`, error categories, runtime helpers, API/internal outputs | Existing C++ golden outputs and functional C++ tests |
| Runtime and binding core | Common conversion/runtime model, name resolvers, ownership, cache and lifetime contracts | Native conversion and lifetime regression tests |
| Dart | FFI then Dart source, finalizers, async and ownership semantics | Existing Dart smoke outputs and functional tests |
| Apple | CBridge then Swift source, nullable/external/generic/ownership behavior | Existing Swift smoke outputs and platform functional tests |
| Android | JNI then Java/Kotlin source, platform annotations, async decorators, parcelable behavior | Existing Android smoke outputs and functional tests |
| Frontend fidelity | Complete all Kotlin validators, filtering/tags, full attribute semantics, Limedoc references/placeholders, warnings/strict mode | Canonical-model comparisons and differential diagnostic cases from existing unit tests |
| Tooling compatibility | Options files, all CLI options, caching/stale-file handling, split outputs, CMake/Gradle integration and distribution | Existing launcher/build integration tests and packaging checks |
| Cutover | Define compatibility guarantees, publish migration guide, performance measurement and release policy | Full supported-platform parity matrix before replacing the JVM tool |

Preserve the preview's stable public boundaries where practical, but avoid
declaring its JSON schema or C++ ABI final before the corresponding parity work.
