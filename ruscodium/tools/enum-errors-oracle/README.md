# Focused M15 enum-backed exception oracle

`check` invokes the installed, unchanged JVM loader and C++ generator in a fresh
process for each group and compares their complete output inventories, actual
source sets, file bytes, and independently projected model facts with native
real-LIME generation. It builds the native library inventory example and the
ordinary `compile-cpp` CLI. The CLI runs with empty `PATH` and no `JAVA_HOME`,
using only LIME, options, and the production templates. It checks the installed
jar's complete production template corpus against source first. For the
baseline, owner, default and custom cases, all generated C++ sources and the
matching consumer are compiled and run independently for the JVM, native
library and CLI outputs with C++17 and strict warnings.

```sh
source /workspace/.ruscodium-env/activate
source /workspace/.gluecodium-env/activate
ruscodium/tools/enum-errors-oracle/check
# Retain the fresh jobs and outputs for inspection; the path must not exist:
M15_ORACLE_OUTPUT=/tmp/m15-enum-inspection ruscodium/tools/enum-errors-oracle/check
# Save source, tool, options, template, job and complete inventory hashes:
M15_ORACLE_REPORT=/tmp/m15-enum-evidence.json ruscodium/tools/enum-errors-oracle/check
```

The main group loads two LIME input files and one auxiliary file. It exercises
cross-file and nested synchronous instance/static throwing functions, two ordered
marked enums within one owner, void and non-void
returns, a nullable return, a renamed top-level enum, two main exceptions that
share a payload enum (one has an explicit C++ name), and an unused main exception that marks that enum for
error-code generation. That exception's default C++ name deliberately collides with
the enum's renamed output name, and exception declarations themselves own no generated
files. A separate main enum referenced only by an auxiliary exception stays an
ordinary enum; a main exception references an auxiliary enum without creating an
auxiliary output. A main method refers to an auxiliary exception whose payload
is the main error enum. The consumer checks implicit enum-to-error-code
conversion, error category names, known and unknown messages, void success and
error returns, and successful and failed `Return` values, including a nullable
value. Separate groups check static class and struct throwing methods, and an
exception-only main input that emits just the 18 common and export files. Fresh
JVM loads also check changed names, enum values, package and throws target. The
default and custom groups use actual default options and configured root and
internal namespaces, exports and copyright, respectively. The checked-in
`evidence.json` records one completed run, including per-file hashes and actual
source sets; neither it nor frozen output is used as native input. Auxiliary-only payload declarations
are checked through output ownership and model projection; no absent auxiliary
header is fabricated.

The bounded projection extends the existing frontend adapter projection with
`LimeException.errorType`, `LimeThrownType`'s type and comment, and the
function's exception target. When the JVM supplies its computed exception
getter, the projection checks it against the independently followed thrown type;
when the native job omits that getter, it derives the same fact from the model.
Adversarial mutations to the error payload, thrown edge and JVM getter must each
change the projection or fail validation. The comparison preserves direct and
resolved type targets and nullability and rejects unknown node fields. Jobs are
comparison evidence only and are never input to native generation. This focused
fixture does not claim support for enum aliases, non-enum payloads, external
payloads, throwing constructors, accessors, lambdas, or asynchronous functions.
Historical captures and previous milestone evidence are not modified.
