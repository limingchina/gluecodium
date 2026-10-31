# JVM template oracle

This tool calls the installed, unchanged Kotlin `TemplateEngine.render` and
records UTF-8 bytes for Rust replay. It needs a Java 17 JDK (`JAVA_HOME` or
`PATH`) and an already installed Gluecodium distribution under
`gluecodium/build/install/gluecodium/lib`. No network or Rust compiler is
needed. From the repository root:

```sh
ruscodium/tools/template-oracle/check
# Intentionally replace all golden files after reviewing a change:
ruscodium/tools/template-oracle/run
```

`check` first compares the complete set of 315 templates inside the installed
Gluecodium jar to the corresponding source files, then runs negative checks,
renders 34 cases into a temporary directory and compares every request and
output byte. `run` renders every
case and constructs every request in memory before writing any fixture. A
render or graph-export failure therefore does not replace a subset of the
fixtures. Each request has an adjacent `.expected` file, including empty
output and outputs without a trailing newline. `oracle/*` templates are
focused test inputs under this tool; `cpp/*` paths refer to unchanged
production templates.

The original fixtures were captured from checkout
`572f7108be2379c0810ff8130617776874a92cfb` (upstream source baseline
`2044ae5c73e8b9521fac6dec6cd6133086dd4136`) using Temurin OpenJDK
17.0.16+8 and `gluecodium-14.2.2.jar` SHA-256
`fe1bda6ef33ef0abdf6c99abb3af9897b0307bb21050e107563368e7b2a8fac2`.
The runtime check compares template contents directly, so it also catches a
stale installed distribution. Exact production-template corpus provenance is
tracked in [TEMPLATE_SURFACE.md](../../TEMPLATE_SURFACE.md).
The `review-helpers` and `review-scope` fixtures were captured from checkout
`7a4ede941bd4dd6737dcc618f6212b5b21a0ffba` using the same JDK and jar.
The `empty-filter`, `review-selectors`, and `review-values` fixtures were
captured from checkout `949eef269` using the same JDK and jar.
The `review-sort` and `review-attributes` fixtures were captured from checkout
`53f639c37` using the same JDK and jar.

The model cases load [fixture.lime](fixture.lime) with the unchanged JVM
loader. `cpp-enumeration` renders three enumerators, a literal value, normal
comments and deprecation; `cpp-alias` uses a list alias; `cpp-function` covers
multiple primitive/string parameters and a const attribute; and the two
`*-throws` cases use nullable alias and enum parameters with an enum-backed
exception. `cpp-function-static` covers a callback parameter, static and
noexcept flags, and multiple C++ attributes. `cpp-return` exercises the ordinary
return path. `name-arguments` exercises zero through three resolver arguments,
including getter and setter modes, against a real model field. The template is
rendered directly with the selected model object as its root; no generator
outer context is supplied, so the throwing return example intentionally has
an empty `internalNamespace` and emits `::Return`. `export-default` and
`export-empty` provide plain map contexts. The helper cases measure truth,
context/set, iteration, inline and named partials, indentation, prefixes,
join, joinPartial, dynamic eval, CR/CRLF prefixes, escaping, missing values and
adjacent standalone tags. `model-helpers` records predicate, sort and class-name
checks against real enumeration nodes. `nested-comment` is a negative compile
check: Trimou rejects a start delimiter nested inside a comment. `review-helpers`
records quoted equals signs and literal backslashes, null equality, repeated
switch defaults, Unicode capitalization, and escaping control characters;
`review-scope` records the iteration index and position. The oracle also
compiles invalid `if`, `unless`, `set`, and duplicate inline-partial definitions
and renders an `each` over a scalar. It requires the actual Trimou exception
class and error code at the expected phase for each, so an unrelated failure
cannot satisfy a negative check. Additional negative checks verify helper
arity, `setJoin`'s required delimiter, and the section-only `if` form even in
inactive branches. The null `capitalize` and `escape` checks verify the JVM's
render-time `NullPointerException`, as does `joinPartial` with a null list.

`review-selectors` records ordinary tag lookups whose names resemble literals
and an `eval` key containing a closing bracket. `review-values` records Java
UTF-16 string lengths, null arguments to `each`, and case-insensitive prefix
options. `empty-filter` renders using the actual C++ predicate registry and
asserts that no predicate was called for the empty input. Its optional
`hooks.registered_predicates` array records the registry's sorted names; its
empty `hooks.predicates` array records that no receiver-specific result was
observed. An unknown predicate is deliberately rejected at the native replay
boundary even though the JVM filter silently skips it.
`review-sort` measures absent iteration metadata while traversing the actual
C++ topological sort result. `review-attributes` exports a JVM-built
`LimeAttributes` instance through the reference snapshot and measures case
and camel-case lookups of its C++ and Swift attribute values.

Each model request embeds the existing version-1 reference snapshot. Node IDs
are assigned by identity before capturing calls. The oracle wraps the actual
`CppNameResolver`, `CppFullNameResolver` and `CppGeneratorPredicates` created
with the default `GeneratorOptions` naming rules, empty C++ root namespace,
`internal` internal namespace and Doxygen comments. It records their individual
input identities and results. It does not record template output as helper
results. `property_overlays` contains only observed public computed getters:
`LimeComment.isEmpty`, `LimeReturnType.isVoid`, `LimeFunction.exception`,
`LimeEnumeration.uniqueEnumerators`, and `LimeType.actualType`. These augment
the bounded snapshot without changing its schema. In `absent_properties`, a
small allowlist of context keys is recorded only after checking that no public
zero-argument Java bean accessor exists on that model object. This establishes
known absent lookups separately from getter values and allows outer-context
lookup while preserving errors for unknown model views. A failing getter is
never treated as absent. The `model-helpers` case records the actual C++ topological sorter input and
result; empty sorter arrays indicate that no sort was used in that case.

The recorded hooks are an explicit offline record/replay boundary. Passing
these fixtures demonstrates a bounded renderer/view contract, not an
implementation of C++ name resolution, complete model projections, generated
file parity, or ABI parity. Full generator ambient context, additional selector modes and broader model
shapes remain future coverage.


## Native C++ name profile

The five `native-*` fixture pairs were captured from the real JVM loader and
resolver using [native.lime](native.lime), the same installed jar and JDK as
the original fixtures, on the M8 implementation checkout based on commit
`1b456d4a2`. Their snapshot roots are the whole actual `LimeModel`; `data`
retains the selected object or matrix for rendering. They retain the JVM's
recorded name calls in `hooks.names` for comparison. A native render test
must remove those calls and add `native_cpp` with the corresponding settings:

| Fixtures | `root_namespace` | `internal_namespace` |
| --- | --- | --- |
| `native-enumeration`, `native-alias`, `native-function`, `native-return` | `[]` | `[]` |
| `native-matrix` | `["outer", "api"]` | `["detail", "impl"]` |

The first four use the unchanged production templates. The input deliberately
has no comments, but every `isEmpty` overlay is obtained from a real JVM model
getter. The matrix uses the tool-owned `oracle/native-names` template to record
individual resolver calls for declarations, qualification, type references,
primitive type IDs, literals, constant references, field/property accessors,
null accessor results, aliases, nullable types, generic types and attributes.
Its renamed enclosing class and nested struct ensure fully qualified names use
actual parent attributes. It also captures mixed acronym and underscore cases.
The recorded matrix has 162 calls and the four production fixtures have 13;
predicates and sorters, where called, remain explicitly recorded JVM hooks.
The matrix config deliberately exercises nonempty root and internal namespaces;
the production fixtures use the actual `GeneratorOptions` empty defaults.
These records establish a bounded differential surface, not whole-generator
parity or support for nonempty comment processing.
