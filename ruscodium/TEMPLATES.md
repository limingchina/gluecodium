# Experimental native template runtime

The Rust renderer executes a bounded compatibility slice of the existing Trimou
Mustache dialect against JSON data and the experimental reference-model snapshot.
It reads the original `.mustache` files directly and never starts a JVM. It is
not yet a replacement for the Kotlin compiler, a complete template model, or a
C++ generator. Parsing the corpus does not imply every helper or model getter is
implemented.

```sh
ruscodium render --templates ../gluecodium/src/main/resources/templates \
  --request tests/template-goldens/cpp-enumeration.request.json --output /tmp/result
```

Omit `--output` to write the completed result to stdout. The renderer completes
validation and rendering before opening the output file. The Rust API is
`ruscodium::template::render(template_root, &serde_json_value) -> Result<String,
String>`; `parse` and `Graph` are also public. Errors cover malformed syntax,
unsupported operations, missing replay entries, invalid graphs and file access.

A version 1 request is a JSON object with `schema` equal to
`gluecodium.template.render-request`, `version` 1, `template` (relative name
without `.mustache`), and `data`. The optional `snapshot` is the distinct
`gluecodium.reference-model.snapshot` version 1 graph described in
[reference-model](tools/reference-model/README.md); `$ref` values in data,
properties and hooks refer to its node IDs. The importer validates IDs, graph
references, node classes and overlays; sharing and cycles are represented by IDs,
not recursively copied. Optional `property_overlays` maps node IDs to measured
computed getter values omitted by the snapshot. An overlay conflicting with a
stored value is rejected.

The experimental optional `absent_properties` maps node IDs to arrays of
property names whose absence was verified by JVM reflection. These are not
missing getter values: they explicitly allow ordinary Mustache lookup to continue
through enclosing contexts, or return null for `this.property`. The importer
rejects unknown IDs, duplicates, and any absence contradicted by a stored or
overlaid property on a node of that class. An unmeasured missing model property
remains an error. Missing plain-map keys behave as null.

Optional `hooks` has `names`, `predicates`, `sorters`, and
`registered_predicates` arrays. Each name entry
has `receiver`, `resolver`, `mode` (`name`, `getter`, `setter`, or `ref`) and a
string or null `result`. Predicate entries have `receiver`, `name` and a boolean
`result`; sorter entries have `name`, list `input`, and list `result`. Receiver
identity is represented by the original graph value, including `$ref` IDs.
Identical repeated entries are permitted; contradictory duplicates are errors.
`registered_predicates` contains distinct, nonempty names from the caller's
actual predicate registry; a recorded predicate result also establishes that
its name is registered. This separate list permits an empty filter without
inventing a predicate result. Every evaluated receiver still needs a matching
result entry. A null receiver for `resolveName` requires a recorded name entry
for its resolver and mode, but does not require a fabricated null result.
Missing entries are errors. These hooks replay externally measured results. Every
computed getter, absent property, hook, and ambient context value must come from
the caller or a documented native projection, not a fabricated default.

An optional `native_cpp` object selects the bounded native C++ name resolver.
Its `root_namespace` and `internal_namespace` fields are arrays of ASCII C++
identifier components, both defaulting to `[]`; unknown options are errors.
For the older oracle configuration use `{"root_namespace":[],
"internal_namespace":["internal"]}`. Native requests must omit or empty
`hooks.names`. Selectors `""`, `"C++"` and `"FQN"` are registered directly;
the `ref` mode is unsupported. Predicates, sorters and property overlays still
use the measured replay contract. The public library entry point
`template::native_cpp::resolve` also resolves one receiver against a `Graph`.

The native slice includes default ASCII C++ naming, qualified declarations,
primitive and generic types, nullability, aliases, basic literals and accessor
names, subject to the model facts present in the snapshot. A nested declaration
requires its actual parent nodes, including their attributes. Missing parents,
nonempty or unavailable comment content, external descriptors, unsupported
C++ attributes, complex values and custom rules report errors. This is not a
complete C++ backend or a replacement for the canonical frontend model.

The runtime parses comments (including Trimou multiline comments), escaped and
unescaped interpolation (both unescaped as configured upstream), nested and
inverted sections, quoted and named arguments, standalone tags, partial
indentation, and forward inline partial definitions. It implements scoped
`set`/`setJoin`, `if`/`unless` including per-argument logic, `each`, `join`,
`joinPartial`, `prefix`, `prefixPartial`, `include`, `eval`, `resolveName`,
`ifPredicate`/`unlessPredicate`, `sort`, `filter`, `instanceOf`/`notInstanceOf`,
`isEq`/`isNotEq`, `capitalize`, `escape`, and the common `switch`/`case`/`default`
flow. The `if` and `unless` default logics differ, as in Trimou. List iteration
supplies one-based `iter.index`, zero-based `iter.position`, and boolean iteration
flags. `capitalize` supports an ASCII initial character and the measured `ß`
mapping; other non-ASCII initial characters are rejected pending Unicode
titlecase compatibility.
Unsupported helpers, hash options (including conditional `else` and join
lambdas), unregistered selectors, and unknown model properties fail rather than
silently emit incomplete output. Some optional features such as `numExpr` remain
unimplemented.

Native views are intentionally small: ordinary JSON maps, scalar strings and
lists; list indexing, `size` and `isEmpty`; string `length` (UTF-16 code units) and
`isEmpty`; enum class identity; and the `LimeBasicType.TypeId` `toString` tags.
`LimeAttributes` uses its documented case-insensitive Map interface, with
snapshot enum keys converted to their attribute tags. Model properties otherwise
come from the snapshot or supplied overlays. Arbitrary Kotlin reflection,
computed documentation, external-platform descriptors and arbitrary Java object
`toString` are not available. A null/missing map value and an unavailable model
getter are deliberately different outcomes.

The internal `$ruscodium.attribute-view` key is reserved and rejected in
request and snapshot values. It represents case-insensitive attribute-value
maps during rendering; ordinary JSON maps retain case-sensitive keys.

Partial names must be relative paths below the canonical template root, without
`.` or `..` components; canonicalized symlinks may not escape that root. The
runtime limits template and request sizes, nesting, partial recursion, and output
size. These bounds and the pre-write behavior are tested, but do not turn the
experimental snapshot into a complete untrusted-input security boundary.

The checked-in JVM-oracle fixtures and their reproduction instructions are in
[template-goldens](tests/template-goldens/) and
[template-oracle](tools/template-oracle/). Their byte comparisons cover selected
real C++ template fragments and measured helper behavior; they do not establish
whole-file or compiler parity.
