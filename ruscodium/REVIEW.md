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
