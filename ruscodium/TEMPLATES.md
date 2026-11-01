# Experimental native template runtime

The Rust renderer executes a bounded compatibility slice of the existing Trimou
Mustache dialect against JSON data and the experimental reference-model snapshot.
It reads the original `.mustache` files directly and never starts a JVM. It is
not yet a replacement for the Kotlin compiler or a complete template model.
Parsing the corpus does not imply every helper or model getter is implemented.

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
the `ref` mode is unsupported. Optional boolean fields `predicates` and `sorters`
default to false and independently select the native C++ providers. Enabled
predicates reject nonempty `hooks.predicates` and `hooks.registered_predicates`;
enabled sorting rejects nonempty `hooks.sorters`. Unknown selectors fail even on
empty input. Disabled providers retain the measured replay contract. Public
library entry points `template::native_cpp::resolve`,
`template::native_controls::predicate` and `template::native_controls::sort`
operate on a `Graph`.

The native slice includes default ASCII C++ naming, qualified declarations,
primitive and generic types, nullability, aliases, basic literals and accessor
names, subject to the model facts present in the snapshot. A nested declaration
requires its actual parent nodes, including their attributes. Missing parents,
nonempty or unavailable comment content, external descriptors, unsupported
C++ attributes, complex values and custom rules report errors. This is not a
complete C++ backend or a replacement for the canonical frontend model.

The predicate provider implements the eleven C++ selectors from raw type, field,
constructor and attribute facts, including actual alias targets, immutable field
traversal and inner-class references. It requires the actual enclosing declarations
for nested paths and rejects missing facts, malformed cycles and unsupported model
classes. Comment text is not exported: an observed empty comment is supported,
and exclusion, deprecation and non-null warnings can establish a result. Nonempty
or unavailable comment text remains unsupported when needed. The sorter filters
non-named inputs and uses the C++ topological dependencies and first-eligible input
order; duplicate full names and cycles are errors. Neither provider reads captured
predicate answers, imported dependency lists, or sorted lists. Measured property
getters remain a separate template-view boundary. The M9 recorded-control
inventory checks 1,095 exact predicate calls and 15 exact sorts; four predicate
calls reject nonempty comment text. Five unchanged class and struct partials match
JVM bytes with all three native providers enabled, including fields, partial
defaults, immutable fields and an explicit field constructor. One class fragment
reorders a nested struct before an alias. The JVM matrix independently records
constructor behavior for immutable list, set, map-value and map-key fields.

For example, turn the recorded full-model enumeration fixture into a native
request, retaining its measured predicate and sorter entries:

```sh
python3 - <<'PY'
import json
from pathlib import Path

request = json.loads(Path('tests/template-goldens/native-enumeration.request.json').read_text())
request['native_cpp'] = {'root_namespace': [], 'internal_namespace': []}
request['hooks'].pop('names', None)
Path('/tmp/native-enumeration.request.json').write_text(json.dumps(request))
PY
cargo run -- render --templates ../gluecodium/src/main/resources/templates \
  --request /tmp/native-enumeration.request.json --output /tmp/native-enumeration.txt
```

To enable all three providers for the recorded full-model class fragment:

```sh
python3 - <<'PYEXAMPLE'
import json
from pathlib import Path

request = json.loads(Path('tests/template-goldens/m9-class.request.json').read_text())
request['native_cpp'] = {'predicates': True, 'sorters': True}
request.pop('hooks', None)
Path('/tmp/native-class.request.json').write_text(json.dumps(request))
PYEXAMPLE
cargo run -- render --templates ../gluecodium/src/main/resources/templates \
  --request /tmp/native-class.request.json --output /tmp/native-class.txt
cmp /tmp/native-class.txt tests/template-goldens/m9-class.expected
```

The CLI is the same `render` command: the JSON request selects native naming.
This template runtime is separate from the preview `-generators cpp` path,
which emits its own experimental `api.hpp`.

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

The separate [`generate-cpp` backend](GENERATION.md) uses this runtime to render
complete files from a guarded full-model job. It always enables native C++ names,
all eleven predicates and the native sorter; callers cannot supply replay hooks
or template contexts. The independent [whole-file oracle](tools/cpp-generation-oracle/)
compares all 50 generated files and source sets across default and custom option
groups, including eighteen common/export files in each group, and compiles and
runs consumers. Its snapshot/getter boundary and unsupported cases are
documented in [GENERATION.md](GENERATION.md). The bounded
[native frontend adapter](FRONTEND_ADAPTER.md) now constructs such jobs from
real LIME for its admitted source subset; complete canonical parity remains open.

Version-2 generation jobs attach a complete raw-comment map internally to the
rendering graph. Native comment names, emptiness and predicates then use the
selection, expansion and guarded formatting algorithms described in
[DOCUMENTATION.md](DOCUMENTATION.md). The standalone version-1 `render` request
keeps its previous contract; it does not accept this raw-comment job field or
gain arbitrary computed Kotlin getters. The documentation oracle adds whole-file
evidence independently of the retained template-fragment fixtures.
