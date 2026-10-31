# Ruscodium

Ruscodium is an experimental native Rust implementation of part of the LIME compiler. It does not depend on the JVM and is not a drop-in replacement for Gluecodium. See [PLAN.md](PLAN.md) for the migration roadmap and [TEMPLATE_SURFACE.md](TEMPLATE_SURFACE.md) for the existing template and model-access inventory and [REVIEW.md](REVIEW.md) for the independent review.

```sh
cargo build --release
cargo run -- -input ../examples/calculator/lime -validate
cargo run -- -input ../examples/calculator/lime --model > calculator.json
cargo run -- -input path/to/lime -generators json -output out
cargo run -- -input path/to/lime -generators cpp -output out
cargo test
```

`-input` and `-auxinput` may be repeated and accept files or directories. Discovery is recursive, sorted and deduplicated; auxiliary declarations participate in lookup but are not generated. `--syntax-only` parses without resolution. `--model` writes the model to standard output; the JSON generator writes `model.json`. `-validate` performs no writes. Long spellings `--input`, `--auxinput`, `--output`, `--validate`, and `--generators` are also accepted. Generation requires `-output`. Unknown options and generators fail. Help and version are available via `--help` and `--version`.

The JSON has `schema_version: 1`, ordered source files, declarations, type references and resolved names. It retains source spans, declaration and type annotations, documentation, accessor declarations, external descriptors, and raw literal spelling. Literal expressions, annotation values, and external descriptors include structured nodes and original text. Return and throws documentation are retained separately. This schema describes the Rust preview model, not the Kotlin LimeModel serialization recommended in the migration plan; it should be considered provisional.

| Area | Preview coverage and limitations |
| --- | --- |
| Syntax | All 345 tracked upstream baseline LIME files parse individually in the corpus test. Declarations, generic and nullable types, annotations, descriptors, and literals are parsed; this is not proof of grammar equivalence. The lexer accepts EOF in place of a final newline, as needed by checked-in inputs. Quoted identifiers containing dots are currently rejected because path segments are not yet represented separately. Some numeric forms, declaration context restrictions, newline placement and expression details still need stricter grammar validation. |
| Resolution | Global and nested type lookup, explicit imports and all enclosing scopes participate in ambiguity detection. Auxiliary files resolve but are not generated. Duplicate named declarations, duplicate parameter/member names, duplicate signatures including alias equivalents, basic type arity, alias/inheritance cycles, inheritance target kinds, field constructor references, throws target kinds, direct invalid Void positions and non-nullable null defaults are checked. This is a subset of JVM validators; defaults and constant references, platform filtering is incomplete. |
| JSON | Versioned, deterministic output for a fixed set of canonical input paths. Source paths are absolute, so output differs when inputs are located elsewhere. |
| C++ | Experimental single `api.hpp`, using LIME package components as C++ namespaces and LIME names as identifiers. Classes/interfaces use virtual methods, virtual destructors and `shared_ptr` references; named constructors become static factory declarations. Struct fields, enums without explicit values, aliases, lambdas, ordinary properties, primitives, strings, blobs, standard containers and nullable values have standalone C++17 mappings. Top-level cross-file dependencies are ordered. No Gluecodium runtime or ABI compatibility is claimed. |
| Remaining targets | Java/Kotlin/JNI, Swift/CBridge and Dart/FFI are not implemented. |

The C++ generator rejects annotations, external descriptors, throws, inheritance, explicit initializers, runtime types (`Date`, `Duration`, `Locale`), references to auxiliary or nested declarations, C++ reserved identifiers, and cyclic by-value dependencies. Some other constructs such as constants, struct instance methods and field constructors are also rejected. Ordered Set elements and Map keys are limited to non-null primitive, string, and enum types; aliases and value types are rejected because their ordering is not established. It renders before creating the output directory, so a backend diagnostic does not leave generated files. Nested declarations can be emitted, but references to them are currently rejected. The output is an API sketch rather than Gluecodium-compatible generated code. Do not use it for production integration.

The corpus test checks the 345 upstream baseline inputs separately because smoke scenarios reuse names. Additional tests validate the calculator and selected coherent smoke groups, and compile and execute a C++17 consumer as well as two checked-in C++ export fixtures. An independent comparison of 49 smoke scenarios with the JVM found Rust success on 46; three (`defaults_const`, `name_clash_overloads`, and `skip`) encounter duplicate names that require Gluecodium's platform filtering. The JVM `comments` scenario also requires extra documentation configuration. The preview is deliberately stricter than JVM validation in some cases: for example, it rejects duplicate parameters and invalid direct `Void` positions that the JVM validation command can accept. The preview also treats alias nullability as inherited for defaults and overload identity; the JVM currently behaves differently in those cases. Neither corpus acceptance nor these comparisons establish complete frontend or output parity.

`cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`, and `python3 -m unittest discover -s tools/tests` are the local checks. The corpus count excludes this port’s own negative `.lime` fixtures; the repository now tracks 348 LIME files in total. The Rust tests compiling C++ require an available `c++` compiler; the corpus inventory test uses `git ls-files`.

The experimental [JVM reference snapshot tool](tools/reference-model/README.md) records a bounded view of the existing model for migration research. It is separate from the Rust runtime and is not yet a canonical adapter or Rust model importer.

The migration will keep the existing Mustache templates unchanged. A future Rust engine must reproduce Trimou helper, reflection, lookup, partial, and whitespace behavior; its implementation is not yet selected. The next phase will compare unchanged representative templates and byte-exact output against the JVM.
