# Guarded native C++ whole-file generation

`ruscodium generate-cpp --job FILE --templates DIR --output DIR` consumes a
version-1 or version-2 `gluecodium.cpp-generation-job` JSON object. The library
entry point `cpp_generation::generate` returns the complete in-memory inventory, including
relative path, `MAIN` or `COMMON` source set, and contents. The separate
`write_files` step validates paths and existing symlinks before creating any
outputs. An I/O failure during writing can leave a partial update. Existing
unrelated files are retained. The earlier `-generators cpp` preview is a separate
backend and does not consume this job format.

For native LIME input, use [`compile-cpp`](FRONTEND_ADAPTER.md). Its bounded
adapter constructs a version-2 job from the Rust model and calls this same
generator, without importing a JVM snapshot or invoking Java.

Both versions accept `schema`, `version`, `snapshot`, optional
`property_overlays`, `absent_properties`, and `options`. Version 2 also requires
`raw_comments`, a complete map of raw ordered comment sections, and forbids
comment `isEmpty` overlays. Version 1 rejects this field. See
[DOCUMENTATION.md](DOCUMENTATION.md) for the exact boundary and formatting subset.
Options are
`root_namespace` and `internal_namespace` arrays, `export`, `export_common`,
and nullable `copyright_header`. Namespace defaults are empty; export defaults
to `_GLUECODIUM_CPP`, common export to the main export, and copyright to null.
Identifier components and macros use ASCII C++ identifier spelling. The
snapshot must contain the full `LimeModel`, main and auxiliary roots, reference
map, enclosing declarations, and builtin types. Only the stored field shapes
listed in `validate_snapshot_shape` are admitted. Contexts, output inventories,
includes, replay hooks, resolved C++ names, and selected templates are not job
inputs.

The measured getter overlay boundary comes from the JVM reference-model oracle
in `tools/cpp-generation-oracle`, using Kotlin frontend getters. Permitted views
are LIME `name` and `fullName` on named elements; `actualType` on types;
`isEmpty` on comments in version 1; `isVoid` on return types; `exception` on functions;
`uniqueEnumerators` on enumerations; `uninitializedFields` on structs; and
`fields` and `struct` on field constructors. Getter values must have the
expected kind and class. Native generation recomputes path names, return void,
uninitialized fields, unique enumerators, and constructor fields and owner from
raw graph facts; it does not use overlays as precomputed C++ names or generator
decisions. Version 1 retains measured comment emptiness because the reference
snapshot does not expose private comment text; nonempty placeholders, excluded
or nonempty comments and unavailable empty-comment views fail its preflight.
Version 2 derives comment views natively from the raw sections and supports the
bounded documentation subset. In both versions, an external descriptor,
inheritance, exceptions/throws, unknown attribute or unknown model class fails
preflight. Repeated mapped C++ method and property-accessor names are also
rejected until the upstream overload validator is ported. The sole accepted
attribute is `@Cpp(Name)` with an identifier value.
Absences are restricted to the measured lookup-fallback names in the validator;
these do not authorize injecting generator context. The native renderer also
supplies verified absent lexical names for its own header and property partials.

For accepted inputs, classes/interfaces, structs, enumerations, aliases and
lambdas use upstream template selection and file ownership; classes/interfaces,
structs and enums have a header and implementation, while aliases and lambdas
have headers. The complete output includes the thirteen common headers, three
common implementations, and two export headers. Header and implementation
imports and forward declarations are derived from graph references, including
nested types. The unchanged production templates are rendered with native name,
predicate and sorting providers. Literal and null values are supported; other
value variants are rejected. Type and value cases beyond the existing native
name/control implementation are rejected when encountered, rather than replayed.

Whole-file JVM comparisons currently cover:

| Fixture | Model cases | Options and output |
| --- | --- | --- |
| `default` | Enum with explicit integer; list alias; lambda; interface with synchronous method, read/write, read-only and static properties; struct with integer and string fields, integer default, nullable integer, map, set and field constructor; nested aliases declared in dependency-reversed order. | Default options; 26 files. |
| `custom` | Renamed class with nested struct and alias, interface and cross-root class forward references, list and nullable class reference, auxiliary root. | Root and internal namespaces, distinct exports, multiline copyright; 24 files. |

Every file's UTF-8 bytes and source set are compared against a fresh JVM
`CppGenerator` capture. The generated C++ implementation files and consumers
are compiled and run with C++17, `-Wall -Wextra -Werror` by
`tools/cpp-generation-oracle/compile-consumers`. The fixtures are evidence for
these combinations, not a claim of full language, frontend, ABI or platform
backend parity. Version-2 documentation fixtures and separately loaded upstream
files are documented in [DOCUMENTATION.md](DOCUMENTATION.md). Equality, error
enums, async, full Markdown/documentation links, filtering, custom
naming rules, other annotations, external bindings, and unimplemented value
variants remain outside this guarded contract.
