# Independent preview review

Reviewer: Sol 6.1, xhigh effort, as requested. Date: 2026-10-31.
Baseline: `2044ae5c73e8b9521fac6dec6cd6133086dd4136`.
Final reviewed code: `2874511cf651161818e4fd39b919f006118d349b`, including
reference snapshot fixes through `663d840dc`.

This review inspected the Rust frontend, resolver, CLI and C++ backend, Python
inventory/comparison tools, experimental Java snapshot tool, tests and scope
documentation. It used small independent fixtures, JVM validation comparisons,
and compiled C++ consumers. All material findings reported in this review were
fixed or given explicit backend rejection before the final recheck. This is a
review of the documented native preview, not approval of full Gluecodium parity.

## Material findings and disposition

| Priority | Reproduced problem | Final behavior and regression evidence |
| --- | --- | --- |
| High | An ordinary `property p: Int` lost its implicit setter; a quoted user type named `Int` became the primitive integer type. | Default setters are emitted; `TypeRef.builtin` preserves the distinction and `Box.v` resolves to `x.Int`. Covered by `review_regressions` and `quoted_builtins_and_cpp_guards`. |
| Medium | Generation succeeded with invalid C++ for reserved identifiers, methods named after their owner, generated property/member collisions, and package/type namespace collisions. | These cases fail before output writes. Distinct legal method overloads remain accepted. Covered by the C++ guard, overload and namespace regression tests. |
| Medium | Struct instance methods became pure virtual and made value structs abstract; mutually referring classes were rejected as a by-value cycle. | Struct instance methods are explicitly unsupported; forwarded class/interface references no longer create value-dependency edges. |
| Medium | `Set<Key>` and `Map<Key, Int>` with a generated struct key compiled as declarations but failed when a consumer inserted a key. | The backend conservatively accepts only proven ordered key types and rejects the others before emission. A string-set/enum-map consumer compiles and runs. |
| Medium | Several malformed declarations and literals passed syntax checks: constructor return types, missing constant initializers, setter-only properties, invalid literal postfixes, nullable exception payloads, multiline annotation strings and invalid generic arity. | The reported forms now fail parsing, including syntax-only mode. Targeted JVM checks confirmed their rejection. Regression tests cover these forms and CR-only line endings. |
| Medium | Nested `Void` escaped validation, and nullable aliases were handled inconsistently by defaults/signatures. | Recursive `Void` checks and alias normalization are tested. Alias nullability is an explicitly documented preview deviation: the JVM behaves differently for these cases. |
| Medium | The reference snapshot omitted lazy resolved type/element targets, and a missing directory could silently produce an empty model. | Explicit bounded target getters preserve identity edges. Missing/empty sources and real unresolved references fail while preserving existing output. The unresolved test now uses a legal field name. |

## Final verification

- `cargo fmt --check`, offline Clippy for all targets with `-D warnings`, and
  offline Cargo tests passed: 22 integration tests, including all 345 baseline
  tracked LIME inputs, coherent repository models and C++ consumers.
- All four Python tool tests passed.
- The reference exporter passed `bash -n` and its full test script, including
  deterministic snapshots, main/auxiliary target identity, literal preservation,
  unresolved references, invalid discovery and unchanged output on failure.
- An independent final rerun of 44 accumulated fixtures had no unexpected
  outcomes. All ten successful generated headers compiled with
  `-std=c++17 -Wall -Wextra -Werror`.
- Three additional ordered-container fixtures checked two guarded failures and
  compiled/executed a consumer inserting into `Set<String>` and an enum-keyed map.

## Remaining boundaries

No reported material finding remains unresolved within this bounded recheck.
Complete grammar rejection, structured diagnostic objects, full validation and
metadata fidelity remain unfinished. Dotted quoted identifiers are explicitly
rejected; platform filtering, constant/default reference semantics, and all
upstream validators are not implemented.

The C++ backend remains a standalone declaration preview. It rejects runtime
features, initializers/constants, annotations, inheritance, nested/auxiliary
type references and other documented unsupported constructs. Compilation of
selected consumers does not establish output, runtime or ABI parity.

The JVM snapshot is provisional and distinct from Rust model JSON. Its bounded
view still omits comment text and platform descriptor contents as documented;
there is no canonical adapter or Rust snapshot importer. The template inventory
is lexical evidence only. The chosen migration path preserves the existing
Mustache templates and implements their Trimou behavior; that runtime and
byte-for-byte generator compatibility remain deferred.

## Native Mustache continuation review

Reviewer: Sol 6.1, xhigh effort, as requested. Date: 2026-10-31.
Final reviewed runtime: `c8b8d8d7e`, including JVM oracle fixtures through
`185053859`. This section records the subsequent template milestone; the preview
review above remains a historical record of its earlier implementation.

The continuation review covered the native parser, renderer, identity-graph
importer, render CLI, JVM oracle, bounded public snapshot API additions and scope
documentation. Independent probes used the installed, unchanged Trimou engine
and actual helper registrations. The review evaluated the documented P1a slice:
stored and measured model views plus explicit name, predicate and sorter replay.
It did not reopen the standalone C++ preview or require a native C++ resolver.

### Findings and disposition

| Reproduced problem | Final behavior and regression evidence |
| --- | --- |
| Unknown model properties could fall through to an outer context and hide an unavailable getter. | Unknown model views fail immediately. Only explicit, measured `absent_properties` permit outer-context lookup; conflicting absences and overlays are rejected. |
| Helper argument parsing confused quoted equals signs and literal backslashes; null equality, iteration position, repeated defaults and Unicode capitalization diverged from Trimou. | JVM fixtures preserve the measured behavior. Position is zero-based while index is one-based; only the first default executes. Capitalization supports ASCII and the measured `ß` mapping, with other Unicode initials explicitly rejected. |
| Invalid helper counts and tag forms could succeed, including inside inactive branches; missing `setJoin` arguments or delimiter produced invented output. | Parsing validates registered helper forms and required arguments throughout the AST, along with quoted syntax and inline-partial uniqueness. JVM negative checks assert the compile phase and actual Trimou error code. |
| Ordinary tag names such as `true` and `1` were interpreted as literals instead of context keys. String length counted Unicode scalars and an unsupported string `size` property was synthesized. | Ordinary interpolation and sections use property lookup; helper arguments retain literal evaluation. String `length` counts UTF-16 code units and `size` remains absent, matching measured outputs. |
| An empty filter could succeed with an unregistered predicate because no per-element replay lookup occurred. | Filtering requires registry evidence, supplied by measured predicate calls or `hooks.registered_predicates`. The JVM fixture records actual registered names for a legitimate empty filter without fabricating receiver results. |
| Attribute value maps lost case-insensitive lookup, and sorting injected iteration metadata that the JVM helper never supplies. | A reserved internal attribute view preserves case-insensitive access without changing ordinary maps; external input cannot forge that view. Sorting pushes each result without creating iteration metadata. Actual attribute and sorter JVM fixtures cover both cases. |
| Secondary helper arguments converted maps and lists to JSON text, and several null arguments succeeded despite JVM failures. | Unsupported object string conversion and the measured invalid null operations return errors. Dynamic `eval` resolves supplied key segments directly, including keys containing brackets. |
| Helper output could accumulate beyond the output limit before the outer renderer checked it. | Join, joinPartial, prefix, escape and indentation append through size checks; iteration and sorting also check aggregate output. Moderate oversize regressions verify a diagnostic and preserved CLI output. No OOM stress or general security-boundary claim was used. |

### Final independent verification

- All 19 template integration tests passed, including the unchanged 315-template
  parse inventory, graph and hook validation, strict missing-view behavior,
  traversal and symlink rejection, recursion limits, output limits and CLI
  sentinel preservation.
- The JVM oracle independently verified all 315 installed templates against
  source and regenerated 29 byte-identical render requests and outputs, with
  additional negative compile/render checks.
- Forty-two retained independent CLI probes passed with exact measured output
  or an explicit rejection for unsupported/invalid operations. These include
  eager validation, ordinary literal-looking keys, UTF-16 length, attribute
  casing, sort context, empty-filter registration and object conversion guards.
- `cargo fmt --check` and offline all-target Clippy with `-D warnings` passed.
  The final source recheck also confirmed section-form prefix options and
  incremental helper output guards.

No reported material finding remains unresolved within this bounded continuation
recheck. The runtime executes selected fragments and helper behavior with an
imported identity graph. Name resolution, predicates and sorting remain explicit
offline replay; computed getters and verified absent properties remain supplied
observations. Additional Trimou features, complete template views, a canonical
preview-model adapter, whole-file generation and byte-for-byte compiler parity
remain later milestones, as documented in `PLAN.md` and `TEMPLATES.md`.

## Native C++ naming continuation review

Reviewer: Sol 6.1, xhigh effort, as requested. Date: 2026-10-31.
Final reviewed implementation: `12aac6c45`, including JVM differential fixtures
from `931251088`. This section records the bounded M8 increment and preserves
the preceding reviews as historical records.

The review covered native resolver dispatch, namespace configuration, default
ASCII name rules, actual parent context, type and alias traversal, containers
and hash spellings, literals, accessors, supported attributes, replay isolation
and failure output. Kotlin `CppNameResolver`, `CppFullNameResolver`,
`CppNameCache`, `NameRules`, `NameHelper` and `CppLibraryIncludes` remained the
normative implementation. Two focused JVM probes also constructed actual model
objects to check lambda-parameter rejection and false accessor attributes.

### Findings and disposition

| Reproduced problem | Final behavior and regression evidence |
| --- | --- |
| A `LimeLambdaParameter` received ordinary parameter naming even though the JVM default name rules throw; an unavailable `external` fact could be treated as null. | Unsupported named classes fail before applying name overrides, and the required external facts must be present. `unsupported_or_missing_naming_facts_do_not_succeed` covers these guards. |
| A stored `CPP.ACCESSORS` value of false or null enabled field accessor names, contrary to `LimeAttributes.have`. | False and null leave field accessors absent. A real JVM-built false attribute returned null for both modes; the Rust regression checks both false and null. |
| FQN dispatch unwrapped an unknown class solely because its name ended in `TypeRef`, allowing a forged receiver to succeed. | Dispatch accepts the supported concrete model reference classes and rejects foreign model class identities. The regression and independent CLI probes cover both a custom suffix and a foreign class with a familiar short name. |
| Literal naming accepted an unknown basic type ID or foreign enum identity and returned the raw value. | Literal and boolean-accessor type decisions validate the actual basic type enum and supported IDs. `rejects_forged_type_reference_class_and_literal_type_id` covers the literal failures. |

### Final independent verification

- All eight native naming integration tests passed. They inventory all 223
  recorded name calls: 203 native results match the JVM, while 20 fail for the
  explicitly recorded boundaries of missing owner context (14), comment text
  (four) and unsupported C++ attributes (two).
- All 162 calls in the broader native matrix match. The four unchanged
  production C++ partial fixtures render byte-for-byte with name hooks removed;
  an independent complete matrix render also matches with name hooks removed
  and its nonempty root and internal namespace configuration.
- Thirty-six independent CLI probes passed. Twenty-nine rejection cases checked
  both empty stdout and preservation of an existing output sentinel. The probes
  cover malformed configuration/hooks, mixed replay/native mode, selectors,
  missing facts and owners, duplicate owners, alias cycles, unsupported
  attributes/classes, malformed literal IDs, ASCII acronym/digit spellings,
  parent name overrides and accessor activation.
- Three additional acyclic generic chains of 256, 1,024 and 4,096 levels each
  produced a depth-limit diagnostic with empty stdout. They did not crash or
  emit a partial rendering.

No reported material finding remains unresolved within this bounded review.
This increment supplies native C++ names for the documented graph facts and
keeps legacy name replay available when native mode is omitted. Predicates and
sorters still require measured replay; computed views still require supplied
observations. Nonempty comments, external descriptors, custom name rules,
complex values, a complete canonical model adapter, whole-file generation and
full compiler/output parity remain later work.

## Native C++ predicates and sorting continuation review

Reviewer: Sol 6.1, xhigh effort, as requested. Date: 2026-11-01.
Final reviewed implementation and fixture candidate: `8eecc1b3b`, including
oracle evidence from `30562b676`, controls through `2d4302b58`, and the renderer
whitespace correction in `3c81755f5`. Earlier review sections remain historical
records of their respective milestones.

The bounded M9 review covered the public native control APIs, boolean opt-ins,
provider registration and replay isolation, raw model/type/attribute traversal,
constructor decisions, sibling imports, ancestor skips, default declaration
sorting, malformed-input failures and unchanged production fragments. The
normative algorithms were `CppGeneratorPredicates`, `CommonGeneratorPredicates`,
`CppImportsCollector`, `LimeTypeHelper` and `TopologicalSort`. Existing M8 naming
behavior was checked for regressions without reopening its broader deferred
scope.

### Findings and disposition

| Problem found during review | Final behavior and evidence |
| --- | --- |
| Exclusion on an empty return, parameter, thrown-type or owning constructor comment incorrectly established `hasAnyComment`. | Only the receiver's own comment exclusion contributes directly. Actual JVM comment mutations and the native exclusion regression preserve the source distinctions. |
| Unknown classes, malformed reference objects, invalid actual types and null attribute groups could produce ordinary booleans or be filtered from a sort. Constructor references could be counted without checking their resolved fields. | Explicit reference/class/context and attribute-shape checks reject these inputs. Raw field-constructor references resolve to fields belonging to the structure. Canonical wrong receiver kinds retain their source behavior, and resolved positional type references are supported. |
| Malformed struct members could enter unbounded sorter recursion, while long immutable-struct traversals lacked a separate depth bound. | Concrete member checks and bounded traversal reject malformed or excessive graphs. Independent legal recursive-struct and self-dependency probes still succeed. |
| A temporary comment-proof implementation could hide malformed required facts behind another true condition. | Only unsupported nonempty comment text can remain uncertain while an independent term establishes the predicate. Missing return/context facts and malformed classes or attributes remain errors; dedicated regressions cover those cases. Native comment-string rendering remains a separate unsupported boundary. |
| The control inventory initially accepted arbitrary provider errors as measured results. | Tests pin all 1,095 exact predicate matches, four specific nonempty-comment rejections and 15 exact sorter records, and reject every unexpected error. Generic sorting derives children from raw element/key/value edges rather than supplied `childTypes`. |
| Real class rendering emitted extra blank lines around multiline comments and inline definitions. Initial struct fragments also omitted field/constructor rendering and did not exercise the two distinct generic immutable traversals. | The parser correction in `3c81755f5` matches measured Trimou whitespace. Five unchanged production fragments now include defaults, immutable fields and accessors with a field constructor. JVM list/set/map-value partial-constructor cases require all-fields constructors while the immutable map-key-only case does not. |

### Final independent verification

- `cargo fmt --check`, offline all-target Clippy with `-D warnings`, and the
  complete 66-test Rust suite passed at the final candidate. This retains the
  preview corpus and compiled C++ consumers, all baseline naming/runtime tests,
  15 native control tests and two whitespace tests with measured edge cases.
- The JVM oracle independently regenerated all 41 request/output pairs with
  exact bytes and verified all 315 installed production templates against
  unchanged source. Its negative checks include actual sorter cycles and
  repeated identities.
- All five M9 production fragments match JVM bytes with name, predicate and
  sorter hooks removed. These cover actual nested declaration reordering,
  sibling forward declarations, partial defaults, immutable fields and C++
  accessors. Measured template getter overlays remain separate from the native
  predicate and dependency algorithms.
- Independent CLI probes matched the class golden in all four predicate/sorter
  opt-in combinations. Separate direct-API probes checked malformed reference
  rejection, null attribute-group rejection, skips distributed across a
  function and two enclosing classes, legal recursive struct traversal and
  self-dependency removal. Failure regressions check empty stdout and existing
  output sentinel preservation.
- The updated complete naming inventory has 295 exact native matches and the
  same 20 explicitly bounded rejections, with no new naming error category.

No reported material finding remains unresolved within this bounded M9 review.
The increment provides native C++ names, predicates and declaration sorting for
the documented imported graph facts. Nonempty/native documentation processing,
a complete canonical frontend adapter, whole-header/output-set generation and
C++ runtime or other-language ABI parity remain deferred. Measured template
views and successful fragments do not establish complete compiler parity.

## Native C++ whole-file generation continuation review

Reviewer: Sol 6.1, xhigh effort, as requested. Date: 2026-11-01.
Final reviewed candidate: `6b1de023380c77fb9887a4beb9ccf2b17dedcc5c`,
including generator implementation `ea16f63f4`, whitespace corrections through
`682b44479`, frozen whole-file oracle `294ff8835`, and the final raw-mutation
evidence. Earlier review sections remain historical records.

The bounded M10 review covered the distinct `generate-cpp` CLI and library,
strict versioned job and imported model boundary, native roots and ownership,
header/implementation contexts, include and forward collectors, complete helper
inventory and source sets, unchanged-template rendering, output paths and
preflight failure behavior. Source comparison used `CppGenerator`,
`CppNameRules`, `CppImportsCollector`, the header/implementation/forward
collectors, `CppIncludeResolver`, `CppIncludesCache` and `LimeTypeHelper`.
Existing M8/M9 providers were checked for regressions within their retained
scope rather than reopening deferred naming or language features.

### Findings and disposition

| Problem found during review | Final behavior and evidence |
| --- | --- |
| Caller-added stored properties could shadow generator context. Adding `LimeStruct.exportName` and removing its measured absence emitted a forged export macro. Unknown snapshot properties and model classes were also accepted. | A closed, class-specific snapshot field schema runs before overlay import. Unknown document/node/field keys, foreign or unsupported classes, and stored generator context are rejected. The independent context-injection probe now fails before writes. |
| Getter admission checked keys without sufficiently checking values; malformed booleans, arrays and model edges could become truthy template controls or remain unnoticed. | Stored values and measured getters have primitive, collection and reference-target checks. Model edges require actual graph references, not enum-shaped objects. Type references, builtin IDs and supported child lists receive consistency checks. Independent malformed `isStatic`, `isConstructor`, `isOpen`, `childTypes`, path and type-reference probes now fail. |
| A missing field index, a builtin key mapped to the wrong type, and indexed declarations removed from their owner collections could silently generate a reduced model. | The full model/root/reference-map boundary checks builtin mappings, main and auxiliary ownership, parent relationships, and indexed collection membership in both directions. Missing-field and orphan-function probes now reject. Auxiliary roots remain available for lookup without owning generated files. |
| A measured empty-comment flag could hide nonempty placeholders. Unsupported literals and alias cycles in unused auxiliary declarations escaped validation because they were never rendered. | Comment placeholders and exclusion are guarded across the graph. Global value and alias/generic-cycle preflight rejects an auxiliary Date literal and a self-referencing auxiliary alias before writes. Empty comment text remains an explicitly measured frontend fact. |
| Whole headers exposed Trimou whitespace differences inside recursive inline definitions and after a definition closed beside another section. | Lexical container tracking and boundary handling preserve the measured bytes. Eight additional independent probes match the configured JVM exactly, including recursion, indentation, same-line close/open tags and CRLF; four retained whitespace tests pass. |

### Final independent verification

- At the pinned final candidate, `cargo fmt --check`, offline all-target Clippy
  with `-D warnings`, and all 77 Rust tests passed. This includes eight complete
  generation tests, the collector test, the retained preview corpus and compiled
  consumers, and the existing native names, controls and renderer tests.
- The fresh whole-file JVM oracle reproduced both full snapshots, path sets,
  source-set manifests and every generated byte, and checked all 315 installed
  production templates against unchanged source. Default generation has 26
  files: nine `MAIN` and seventeen `COMMON`. Configured generation has 24:
  seven `MAIN` and seventeen `COMMON`. Each group includes all eighteen
  helper/export files, including the `MAIN` export header.
- Independent native CLI runs with an empty `PATH` matched all fifty frozen
  output files byte-for-byte, then produced identical inventories and contents
  on repetition. Both native-generated sets compiled with C++17,
  `-Wall -Wextra -Werror`, and ran their consumers; each compiled six generated
  implementation files. The JVM-generated consumers passed independently.
- The final fixtures exercise defaults, field construction, properties,
  containers including `Set<String>`, nullable values, cross-root references,
  class forwards, nested includes, configured namespaces/exports/copyright and
  actual dependent-before-dependency nested aliases. Raw type/name/path and
  declaration mutations change native files, includes, forwards, qualified
  names and order without updating captured name/order results.
- Twenty saved independent negative probes now reject with empty stdout and
  byte-preserved existing output. A late missing implementation partial also
  preserves existing files. Separate output-root, ancestor and late-target
  symlink probes, plus a model/helper collision, fail during preflight without
  writing generated artifacts. Final write-phase I/O failures are explicitly
  outside transactional rollback guarantees.
- The retained JVM template oracle reproduced all 41 request/output pairs and
  checked the same 315 templates. Four Python tooling tests and the
  reference-model export tests also passed.

No reported material finding remains unresolved within this bounded M10 review.
The result is complete C++ file-set generation for the documented guarded
snapshot subset, not complete frontend, language-feature or runtime/ABI parity.
Private comment text still requires the measured empty-comment admission.
Canonical native frontend adaptation, nonempty documentation, externals,
custom naming rules, inheritance and overload validation, errors, equality,
async, filtering and other platform backends remain deferred or explicitly
rejected. Measured fixtures do not establish unsupported combinations.

## Independent review: M11 native documentation and smoke inventory

Reviewed on 2026-11-01 by the independent Sol 6.1 xhigh reviewer against the
committed M11 contract `1b3151a81`, baseline `d9dc5b901`, native implementation
`84377ae1e`, documentation `956cc0e62`, and final oracle/report tools through
`1dedc2ac8`. No native source changed after the implementation commit. This
review appended only this section; earlier milestone reviews remain historical.

The review compared `LimeComment`, the C++ comment/name/predicate processors,
Flexmark formatting, loader placeholder construction, unchanged documentation
partials and smoke option handling with the new Rust/importer/oracle paths.
It checked complete raw-comment coverage, ordered section types and IDs,
placeholder targets and keys, global cycles, expansion limits, raw versus
selected emptiness, Kotlin whitespace, exclusion rules, lambda parameter names,
per-file graph import and retained version-1 behavior. The version-2 parent
lookup follows the actual reference map, including absent synthetic parents;
indexed declaration ownership remains validated. The comment-only `@` path
allowance cannot authorize declaration paths.

### Findings and disposition

| Finding during independent review | Final behavior and evidence |
| --- | --- |
| An acyclic graph repeatedly referring to an empty placeholder could do exponential work without reaching the output-size bound. | Expansion is memoized, with independently checked depth and size limits. An 80-node duplicated empty DAG and a 128-level chain complete with unchanged output; a 129-level chain and oversized expansion reject. |
| The first plain-text guard admitted unimplemented setext headings and list markers, including tab separators and bare markers. | Conservative checks reject the measured syntax, including marker lines with trailing whitespace. Fresh JVM counterexamples and focused Rust regressions cover the failures. |
| Trailing mixed tabs/spaces, paragraph-final hard breaks and tabs following a paragraph break could produce different Flexmark bytes or admit indented code. | The unproved forms reject. An independent deterministic sample of 7,203 whitespace, Unicode and marker inputs admitted 1,643 cases; every admitted result matched fresh JVM formatter bytes. Another 40 Unicode whitespace-line cases also matched. |

### Final independent verification

- `cargo fmt --check`, offline all-target Clippy with `-D warnings`, and all
  87 Rust tests passed: four library units, fifteen whole-file generation,
  fifteen controls, eight names, twenty-two preview, nineteen template runtime
  and four whitespace tests. The preview corpus and compiled consumer remain
  covered.
- Fresh JVM checks reproduced all 41 template request/output pairs and all
  315 installed production templates. The legacy whole-file oracle reproduced
  both complete version-1 snapshots, source sets and fifty generated files.
  The default reference exporter and legacy fixtures are unchanged from the
  baseline. Four Python tooling tests and the reference-model tests passed.
- The three new real-LIME captures reproduced all 63 complete JVM files and
  actual source sets: 23 for the focused fixture and 20 for each separately
  loaded, unmodified upstream interface/lambda file. Every raw-comment map
  exactly covers its snapshot's comment nodes, with no `isEmpty` overlays;
  the snapshots remain version 1. Each job includes all eighteen helper/export
  files. The native CLI produced identical inventories and bytes twice with
  an empty `PATH`.
- All generated implementations and meaningful consumers compiled and ran
  with C++17, `-Wall -Wextra -Werror`, for both legacy native groups and all
  three native documentation groups. The corresponding fresh JVM consumers
  passed independently. Each legacy group compiled six generated sources;
  the documentation groups compiled five, four and four respectively.
- Thirty-seven saved independent negative CLI probes rejected malformed or
  incomplete raw maps, wrong pairs/IDs/classes/targets, missing placeholders,
  unused cycles, forged comment answers, unsupported expanded text, auxiliary
  documentation, invalid version boundaries and excessive depth/expansion.
  Every rejection had empty stdout and preserved the complete existing output
  inventory and bytes. Aggregate tests also retain late-template/path failure
  and symlink preflight checks.
- An independent fresh fifteen-case matrix reproduced the checked final
  outcomes, effective options, input hashes, complete JVM output hashes and
  source sets. All baseline case/provenance comparisons matched, including
  Java, the installed JVM compiler jar and all 315 templates. Among thirteen
  complete groups, `namespace_basic` is exact and twelve remain guarded
  rejections, with no output mismatch or JVM/export failure. The two separately
  labeled upstream comment files move from rejection to exact match; the full
  comments group remains rejected. Actual native library source sets and CLI
  bytes agree. The final process-failure classification and compiler/helper
  provenance follow-ups were also reviewed.

No reported material finding remains unresolved within the bounded M11 contract.
This establishes the conservative imported raw-comment documentation profile
and the measured acceptance inventory. Full Markdown and scoped links, native
LIME/Limedoc adaptation, filtering, inheritance, externals, additional attributes,
overloads and broader C++ runtime/ABI or platform parity remain deferred or
guarded. Synthetic recursive-placeholder evidence does not imply that the
configured loader supports nested placeholder definitions. Existing write-phase
I/O rollback limitations are unchanged.
