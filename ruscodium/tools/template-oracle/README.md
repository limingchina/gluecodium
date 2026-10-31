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

`check` first compares every one of the 315 templates inside the installed
Gluecodium jar to the corresponding source file, then renders into a temporary
directory and compares every request and output byte. `run` renders every
case and constructs every request in memory before writing any fixture. A
render or graph-export failure therefore does not replace a subset of the
fixtures. Each request has an adjacent `.expected` file, including empty
output and outputs without a trailing newline. `oracle/*` templates are
focused test inputs under this tool; `cpp/*` paths refer to unchanged
production templates.

The checked-in fixtures were captured from checkout
`572f7108be2379c0810ff8130617776874a92cfb` (upstream source baseline
`2044ae5c73e8b9521fac6dec6cd6133086dd4136`) using Temurin OpenJDK
17.0.16+8 and `gluecodium-14.2.2.jar` SHA-256
`fe1bda6ef33ef0abdf6c99abb3af9897b0307bb21050e107563368e7b2a8fac2`.
The runtime check compares template contents directly, so it also catches a
stale installed distribution. Exact production-template corpus provenance is
tracked in [TEMPLATE_SURFACE.md](../../TEMPLATE_SURFACE.md).

The model cases load [fixture.lime](fixture.lime) with the unchanged JVM
loader. `cpp-enumeration` renders three enumerators, a literal value, normal
comments and deprecation; `cpp-alias` uses a list alias; `cpp-function` covers
multiple primitive/string parameters and a const attribute; and the two
`*-throws` cases use nullable alias and enum parameters with an enum-backed
exception. `cpp-return` exercises the ordinary return path. The template is
rendered directly with the selected model object as its root; no generator
outer context is supplied, so the throwing return example intentionally has
an empty `internalNamespace` and emits `::Return`. `export-default` and
`export-empty` provide plain map contexts. The helper cases measure truth,
context/set, iteration, inline and named partials, indentation, prefixes,
join, escaping, missing values and adjacent standalone tags.

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
never treated as absent. Empty sorters indicate none were used in these cases.

The recorded hooks are an explicit offline record/replay boundary. Passing
these fixtures demonstrates a bounded renderer/view contract, not an
implementation of C++ name resolution, complete model projections, generated
file parity, or ABI parity. Cases with static functions, callback parameters,
C++ `Attribute`, full generator ambient context and additional selectors
remain future coverage.
