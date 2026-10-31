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
P0 has delivered bounded investigation tooling and P1a has delivered a bounded
native template/runtime slice. The complete canonical boundary and subsequent
backend phases remain incomplete until their own acceptance evidence exists.

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
   JVM fixtures. `resolveName`, predicates and sorters replay measured results;
   their C++ implementations have not been ported. Unknown selectors and
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
optional `property_overlays`, optional `absent_properties`, and optional `hooks`.
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

`hooks.names` is a list of `{resolver, mode, receiver, result}` records, with
mode `name`, `getter`, `setter` or `ref` and a string-or-null result.
`hooks.predicates` is a list of `{name, receiver, result}` records with boolean
results. `hooks.sorters` is a list of `{name, input, result}`
records containing ordered input/result value lists. Receivers and list entries
are graph values; equality preserves referenced instance IDs. Identical replay
entries are permitted, while contradictory duplicates and malformed values
fail. Unknown selector names and missing requested results fail explicitly.
A null receiver to `resolveName` needs evidence of the requested resolver/mode
in `hooks.names`, without an invented receiver-specific null result.

Optional `hooks.registered_predicates` contains distinct, nonempty names from
the actual Kotlin predicate catalog. A measured receiver-specific predicate
entry also establishes that its name is registered. The separate catalog
permits an empty filter when no predicate invocation was observed; it must not
be replaced by fabricated per-receiver results. With neither catalog evidence
nor an observed result for a name, even an empty filter fails. Every evaluated
receiver still needs its measured boolean result. This strict rejection of
unknown predicates is intentional even where JVM filtering would skip them.
The serialized hooks remain an explicit offline replay boundary. Native C++
name resolution, predicates, sorters and future helper-provider interfaces
remain implementation work.

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
selected engine/view contract. They do not establish native naming, canonical
model completeness, complete C++ file sets, or runtime/ABI parity.

Full Trimou syntax validation and consistent source-position diagnostics, the
standalone CLI graph inspector, and unimplemented helper/view contracts remain
open within this experimental runtime. The native frontend-to-canonical
adapter, native C++ helper implementations and whole-file compatibility backend
remain pending in the following phases.

### M8 / P1a.1: strict native C++ naming — next bounded increment

Replace the name-hook replay boundary for a measured subset of C++ naming with
Rust calculations from the imported identity graph. Keep all 315 production
Mustache templates unchanged. This is a continuation of P1a, not completion of
P1b, a canonical frontend adapter, or whole-C++ output/runtime parity.

Sol 6.1 max owns this initial plan and its documentation commit; Terra 6.1 xhigh
owns implementation, oracle extensions and evidence; Sol 6.1 xhigh independently
reviews the resulting behavior. Commit this plan/checklist before implementation.
Implementation stays under `ruscodium/`, including any JVM test-oracle changes.

#### Request and resolver contract

Add an optional `native_cpp` object to the existing version-1 render request.
Its presence selects native names; omission retains the existing replay contract.
The initial options are `root_namespace` and `internal_namespace`, each an array
of namespace components, defaulting to empty arrays as in `GeneratorOptions`.
For the existing oracle configuration use
`native_cpp: {"root_namespace": [], "internal_namespace": ["internal"]}`.
Validate types, namespace components and unknown option keys before rendering.
An empty object is an explicit opt-in, not a request to replay captured names.

In native mode reject nonempty `hooks.names`; do not consult name recordings on
any native success or unsupported-receiver path. Keep recorded name cells solely
as expected values in differential tests, outside the request being rendered.
Existing predicates, sorters, registration catalogs, property overlays and known
absences remain explicit replay/measured boundaries. They do not become native
because names are native. Native registration supplies selectors `""`, `"C++"`
and `"FQN"` without fabricated hook entries. Preserve measured helper argument,
mode normalization and null-receiver behavior; unsupported selectors/modes fail.
The upstream `ref` mode is not implemented by these C++ resolvers and remains an
explicit error. FQN uses `CppFullNameResolver` semantics, not a qualified version
of the C++ type-expression resolver.

Build a separate typed native naming module over `Graph`; keep helper dispatch
and name-rule/type calculations distinct. A resolver may cache results it has
computed from model facts, but must not load a precomputed name-result table.
Use actual node classes, `LimePath` head/tail/disambiguator, reference edges and
attributes. Preserve declaration identity, shared references and overload paths.
Index available named model nodes and require all traversable parents needed by
`CppNameCache`. A selected-object snapshot can omit its owning container: missing
parents are unsupported context, never evidence of an unannotated/default-named
parent. Extend native JVM fixtures to snapshot the real full model, or export
the actual required parent nodes, retaining the selected render root in `data`.
Do not synthesize parent nodes or infer their attributes from path strings.

#### Bounded naming surface

Port the checked-in `namerules/cpp.properties` and Kotlin `NameHelper` behavior
for supported ASCII names, including underscore, mixed-case/acronym and getter
prefix cases. Reject unmeasured Unicode casing rather than approximate JVM
locale/Guava behavior. No configurable naming files are supported in this slice.

The required matrix covers ordinary named declarations, parameters, fields,
constants/enumerators, root/package/nested qualification, enum/type-alias names,
`LimeBasicType.TypeId`, type references and return types. Port exact C++ primitive,
string/blob/date/duration/locale type spellings, list/map/set spacing and hash
selection, nullable wrappers, class/interface shared pointers, exception type
mapping, alias identity and alias-aware actual-type decisions. Aliases must not
be flattened when the Kotlin resolver retains their names. Resolve cycles and
missing required facts with bounded diagnostics.

Also cover supported ordinary literals and constant references, property
getters/setters and field accessors where real parent context establishes
`@Cpp(Accessors)`. Test boolean getter prefixes through aliases. Honor only
explicitly ported naming/type attributes, initially `@Cpp(Name)`, accessor
`@Cpp(Name)`, `@Cpp(Type)` and `@Optimized` where the source resolver uses them;
measure each supported interaction against the JVM. Preserve upstream errors
for element/rule combinations unsupported by the default rule set.

Nonempty comment processing, external descriptors, custom naming files and
complex defaults remain deferred unless deliberately added with independent
JVM evidence. A measured empty comment may resolve to the empty string from its
actual `isEmpty` fact. Do not fabricate raw comment sections or store a resolved
C++ comment string as a native projection. Date/locale/duration/special or
aggregate literal handling beyond the supported literal matrix must diagnose
the exact unsupported case. Unsupported attributes or unavailable required
model facts fail before any output write; replay is never the fallback.

#### Acceptance and review

1. Inventory every existing recorded name cell by selector, mode, receiver class
   and support status. Evaluate every supported cell through native resolution
   with `hooks.names` removed and compare its exact string/null result. Retain
   explicit unsupported assertions for the remainder; report counts and reasons
   instead of silently excluding cells. Where an old selected-root snapshot
   lacks parent context, prove its rejection and add a JVM-derived complete
   context case with the same measured receiver/result.
2. Reproduce byte-exact output from unchanged `cpp/CppEnumeration`,
   `cpp/CppTypeAlias`, `cpp/CppFunctionSignature` and `cpp/CppReturnType`, including
   their executed partials and function attributes, with native names and no
   name hooks. Add genuine JVM-loaded comment-free cases where existing
   documentation would execute the deferred comment processor; preserve the
   existing replay fixtures. Add explicit root/internal namespace cases and
   new JVM cells for supported naming/type/accessor combinations absent from
   the old recordings. Record configuration and distribution/input provenance.
3. Reject invalid config, unknown selectors, mixed native/name-hook requests,
   missing parent context, unsupported comments/attributes/externals/defaults
   and cyclic/malformed native model dependencies. Verify existing output bytes
   survive each representative failure and stdout receives no partial render.
   Changing/removing recorded name results must never affect a native render.
4. Run formatting, offline Clippy with warnings denied, Cargo tests, existing
   Python/reference-model checks and JVM oracle reproduction/template equality.
   Retain all preview/corpus/C++ consumer checks and the 315-template corpus
   hash. Update `TEMPLATES.md`, README, oracle docs, TASKS and review evidence to
   distinguish native names from replayed predicates/sorters and deferred full
   backend parity. Obtain the independent review, fix material findings, commit
   tested increments and push the already authorized branch.

### P1b: JSON-consuming C++ compatibility backend — deferred

Implement C++ generation from the canonical snapshots before tying it to Rust
frontend fidelity. Use the template-surface report to implement typed property
views and helper contracts rather than assuming `serde_json` lookup reproduces
Kotlin reflection. Port the name resolvers and configurable name rules together
with the helper layer.

Build on P1a's measured custom runtime and extend the explicit property/helper
contracts through the C++ backend. Template conversion is outside the chosen
approach. Preserve standalone tags, missing/null values, section context, helper
scope, indentation from `prefixPartial`, and final newlines as coverage grows.
The acceptance criterion is byte-for-byte compatibility on existing smoke
outputs, including whitespace; normalizing generated source or merely compiling
it is insufficient. Selected-template equality from P1a does not satisfy this
whole-backend criterion.

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
