# Native LIME to C++ compatibility pipeline

`compile-cpp` connects the Rust loader and resolver to the existing whole-file
C++ backend. It reads real LIME and constructs the backend model natively;
generation does not invoke Java or read captured JVM jobs, snapshots or expected
outputs. The original production Mustache templates remain unchanged.

```sh
cargo run -- compile-cpp \
  --input tools/cpp-generation-oracle/default.lime \
  --templates ../gluecodium/src/main/resources/templates \
  --output out-cpp
```

Repeat `--input` and `--auxinput` for additional files or directories. Inputs use
the existing deterministic discovery and deduplication. A main input, template
directory and output directory are required. Scalar options cannot repeat, and
unknown flags or missing values fail. Auxiliary declarations participate in
lookup without owning output files. This command is distinct from the preview
`-generators cpp` API sketch and the snapshot-driven `generate-cpp --job` command.

Use `--options FILE` for a strict JSON document:

```json
{
  "schema": "gluecodium.native-cpp-options",
  "version": 1,
  "root_namespace": ["acme", "api"],
  "internal_namespace": ["acme", "detail"],
  "export": "ACME_API",
  "export_common": "ACME_COMMON",
  "copyright_header": "Copyright 2026 Example\nAll rights reserved."
}
```

The five generator settings are optional. Defaults are empty namespaces,
`_GLUECODIUM_CPP`, common export inherited from the main export, and null
copyright. Unknown fields, unsupported schema versions and unsafe identifiers
fail before writes. The configuration accepts no model graph, getter answers,
render context or output inventory.

The public library entry points are `cpp_adapter::build_job(&Model, &Options)`
and `cpp_adapter::generate(&Model, templates, &Options)`. Generation returns
`GeneratedFile` records with paths, source sets and contents. The adapter clones
and validates the model, clears resolved-target caches, resolves references
afresh and builds the complete graph required by the existing backend. This
includes builtins, main/auxiliary membership, ownership and indexes, generic and
nullable references, defaults, synthetic accessors and field constructors.
Version-2 raw comment records are native facts; measured JVM getter answers are
not inputs to this pipeline.

The initial compatibility surface includes the existing default/custom fixtures:
classes/interfaces, structs, enums, aliases, lambdas, synchronous members,
properties, supported literal defaults, field constructors, nested types,
containers, nullable references and supported `@Cpp` names. Admission remains
guarded. Top-level and nested exceptions with direct nonnullable enum payloads
and ordinary synchronous instance or static throwing methods are supported.
Enum and exception aliases in these positions, non-enum payloads, throwing
constructors, accessors and lambdas, async, inheritance, external descriptors,
filtering, arbitrary attributes and unimplemented source/model forms fail
explicitly. Exception declarations accept the existing bounded `@Cpp(Name)`
annotation. Throws comments and documentation blocks remain unsupported. Type-position
documentation is retained in `TypeRef.docs` so unsupported metadata can be
diagnosed; the field is omitted from preview JSON when empty. Full frontend and
canonical-model parity remain unfinished.

Additional live JVM cases cover open classes, narrow interfaces, constructors,
static and struct methods, and supported name annotations on nested types and
members. They check byte and model compatibility. Compilation claims apply to
the baseline consumers: integer literals containing underscores currently retain
the JVM's spelling (for example `1_000`), which is invalid C++. That mutation
establishes matching behavior, not successful compilation of that numeric form.

Bounded source documentation is also mapped natively: ordinary `//` comments,
platform sections, exclusion and the supported parameter/return/property/
constructor blocks feed the existing [documentation formatter](DOCUMENTATION.md).
The two unmodified upstream interface/lambda documentation files are acceptance
units. Known parameter blocks are matched by the actual parameter name; an
unmatched block follows the measured JVM behavior. Block comments, placeholders,
type-position documentation, directly attached parameter/accessor/return-type
documentation and unimplemented syntax remain explicit errors. Explicit `@param`
blocks on field constructors are also rejected; their admitted parameter
comments derive from the fields' own descriptions. The options profile has no
placeholder configuration; the focused M11 placeholder fixture
therefore remains a backend regression, not an admitted frontend input.

Adaptation and all rendering finish before `write_files` starts. Input,
configuration, model and template failures leave existing output intact and
stdout empty. The writer retains its documented write-phase I/O limitations and
unrelated-file behavior; see [GENERATION.md](GENERATION.md).

The [adapter oracle](tools/frontend-adapter-oracle/README.md) independently
loads the same inputs in the JVM and compares every generated path, actual
source set and byte. It also compares an explicitly enumerated semantic model
projection, normalizing traversal IDs and allocation artifacts while preserving
meaningful ordering and model facts. Live source mutations, compiled native
consumers and CLI runs from a temporary directory with an empty `PATH` supplement
the baseline comparisons. These establish the supported slice, not complete
canonical equivalence. The dedicated M12 checklist is in [TASKS.md](TASKS.md).

The baseline jobs contain 90 files: 26 default, 24 custom and 20 for each isolated
upstream documentation input. Live JVM mutation cases exercise additional source
forms and model facts. Documentation model comparisons use fresh JVM loads of
the isolated main files; frozen M11 outputs are compared independently, without
claiming equality to their unrelated auxiliary or placeholder configuration.

The focused [enum-errors oracle](tools/enum-errors-oracle/) compares complete
JVM and native output and semantic model projections, including nested and
cross-root payloads, shared and unused exceptions, auxiliary lookup, custom
namespaces and `@Cpp` names. Void methods return `std::error_code`; value
methods use the configured `Return<T, std::error_code>` helper. Main exception
declarations mark their payload enums for category generation even when unused;
auxiliary exceptions do not independently mark enums, and auxiliary roots do
not own generated files. Exception declarations themselves emit no files.
