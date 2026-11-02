# Ruscodium

Ruscodium is an experimental native Rust implementation of part of the LIME compiler. It does not depend on the JVM and is not a drop-in replacement for Gluecodium. See [PLAN.md](PLAN.md) for the migration roadmap and [TEMPLATE_SURFACE.md](TEMPLATE_SURFACE.md) for the existing template and model-access inventory and [REVIEW.md](REVIEW.md) for the independent review.

```sh
cargo build --release
cargo run -- -input ../examples/calculator/lime -validate
cargo run -- -input ../examples/calculator/lime --model > calculator.json
cargo run -- -input path/to/lime -generators json -output out
cargo run -- -input path/to/lime -generators cpp -output out
cargo run -- compile-cpp --input tools/cpp-generation-oracle/default.lime \
  --templates ../gluecodium/src/main/resources/templates --output out-native
cargo run -- generate-cpp --job tests/cpp-generation-goldens/default/job.json \
  --templates ../gluecodium/src/main/resources/templates --output out-cpp
cargo run -- generate-cpp --job tests/cpp-documentation-goldens/docs/job.json \
  --templates ../gluecodium/src/main/resources/templates --output out-docs
cargo run -- render --templates ../gluecodium/src/main/resources/templates \
  --request tests/template-goldens/cpp-enumeration.request.json --output enumeration.txt
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

The preview C++ generator rejects annotations, external descriptors, throws, inheritance, explicit initializers, runtime types (`Date`, `Duration`, `Locale`), references to auxiliary or nested declarations, C++ reserved identifiers, and cyclic by-value dependencies. Some other constructs such as constants, struct instance methods and field constructors are also rejected. Ordered Set elements and Map keys are limited to non-null primitive, string, and enum types; aliases and value types are rejected because their ordering is not established. It renders before creating the output directory, so a backend diagnostic does not leave generated files. Nested declarations can be emitted, but references to them are currently rejected. The output is an API sketch rather than Gluecodium-compatible generated code. Do not use it for production integration.

The corpus test checks the 345 upstream baseline inputs separately because smoke scenarios reuse names. Additional tests validate the calculator and selected coherent smoke groups, and compile and execute a C++17 consumer as well as two checked-in C++ export fixtures. An independent comparison of 49 smoke scenarios with the JVM found Rust success on 46; three (`defaults_const`, `name_clash_overloads`, and `skip`) encounter duplicate names that require Gluecodium's platform filtering. The JVM `comments` scenario also requires extra documentation configuration. The preview is deliberately stricter than JVM validation in some cases: for example, it rejects duplicate parameters and invalid direct `Void` positions that the JVM validation command can accept. The preview also treats alias nullability as inherited for defaults and overload identity; the JVM currently behaves differently in those cases. Neither corpus acceptance nor these comparisons establish complete frontend or output parity.

`cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `cargo test`, and `python3 -m unittest discover -s tools/tests` are the local checks. The 345-file baseline corpus count excludes this port’s own `.lime` fixtures. The Rust tests compiling C++ require an available `c++` compiler; the corpus inventory test uses `git ls-files`.

The experimental [JVM reference snapshot tool](tools/reference-model/README.md) records a bounded view of the existing model for migration research. The native template runtime imports its version-1 identity graph and supports measured property overlays and explicitly absent properties. The library exposes `Graph`, `parse`, and `render`; the CLI renders a request against a template root. The snapshot and preview model JSON are distinct formats, and a complete canonical adapter remains future work.

The [native Mustache runtime](TEMPLATES.md) reads the 315 existing templates unchanged and implements a bounded set of Trimou helpers, lookup and whitespace behavior. Requests can select native C++ naming with `"native_cpp": {}` and independently enable its eleven predicates and default declaration sorter with `"predicates": true` and `"sorters": true`. Each enabled provider rejects its recorded hooks; disabled providers retain the replay contract. The native algorithms use model facts, actual enclosing declarations and default C++ rules. They reject missing facts, unsupported comment content and malformed cycles rather than inventing results. The [JVM oracle](tools/template-oracle/README.md) captures reproducible predicate and sort calls and byte-exact unchanged C++ fragments, including class and fieldful struct partials rendered with all three native providers. Complete model, helper and naming parity remain future work.

For examples of native naming and all three native providers, see the request
conversion and unchanged `render` CLI examples in [TEMPLATES.md](TEMPLATES.md).
This path is separate from the preview `-generators cpp` backend described above.

The separate [`generate-cpp` whole-file backend](GENERATION.md) consumes a strict
versioned job containing a full JVM reference-model snapshot and measured
frontend getter views. It derives paths, includes, forward declarations and
render contexts natively, with all C++ name, predicate and sorting providers
enabled; it runs without a JVM. For its guarded comment-free subset it emits
model headers and implementations plus all eighteen upstream common/export
files. The default and custom JVM fixtures compare all 50 paths, source sets and
UTF-8 file bytes, and both generated consumers compile and run under strict
C++17 warnings. This job format is distinct from the Rust preview model and the
`-generators cpp` API sketch. The bounded
[native frontend adapter](FRONTEND_ADAPTER.md) builds this backend's input from
real LIME. Full canonical-model, C++ feature and ABI parity remain future work.

Version-2 jobs add [native documentation processing](DOCUMENTATION.md) from
ordered raw comment sections, including platform selection, placeholders,
exclusion and a guarded plain-text formatting subset. Version-1 jobs and their
fixtures retain their previous contract. The
[smoke inventory](tools/cpp-smoke-matrix/README.md) records complete-scenario
acceptance separately from the two unmodified upstream documentation files.
Full Markdown, scoped documentation links and complete frontend/canonical-model
parity remain future work.

[`compile-cpp`](FRONTEND_ADAPTER.md) provides the native LIME → Rust model →
compatibility backend path. It accepts main/auxiliary source inputs and strict
generator options, reconstructs the backend graph natively and renders the
unchanged Mustache templates without Java or captured model inputs. The
[adapter oracle](tools/frontend-adapter-oracle/README.md) compares 90 baseline
files across default/custom inputs and two isolated upstream documentation
files, plus model facts and live source mutations. This is the dedicated M12
adapter slice; the snapshot-driven CLI and preview emitter remain separate.

The [original performance experiment](PERFORMANCE.md) compares real Kotlin/JVM and
release Rust C++ pipelines with matched outputs, fresh-process runtime, CPU and
peak RSS, plus a separate persistent-process API test. It records the native
port's small-input advantage and poor larger-model scaling, with raw samples,
reproduction steps and an independently reviewed method. The follow-up
[optimization comparison](OPTIMIZATION.md) measures the original Rust binary,
the optimized generator and Kotlin/JVM on the same host. The generator now
shares prepared graphs and resolver indexes, indexes class properties and
caches parsed Mustache templates with fresh state for each output file.
Both experiments cover the supported workloads; complete compiler parity
remains future work.
