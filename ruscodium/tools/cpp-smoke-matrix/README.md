# JVM C++ smoke acceptance inventory

This inventory runs the thirteen complete upstream smoke groups named in the M11
plan and two separately labeled single-file documentation cases. It reads each
scenario's `commandlineoptions.txt` through the JVM `OptionReader`, substituting
its input and auxiliary directories as `SmokeTest` does. In its absence the smoke
C++ internal namespace is `gluecodium` and internal prefix is `foobar_`. The
report records effective C++ options, tags, placeholders, source/configuration
hashes, generator output hashes and source sets, JVM version and jar hashes,
template hashes, compiler version and native revision. The caller supplies the compiler used to
build the executable; it is not inferred from whichever toolchain is on PATH. The C++ generator gets
the original, unfiltered loader model and applies its own filtering. General
`Gluecodium.validateModel` is not invoked; a JVM load/generator error is reported
separately from export and native errors. The `skip` tags cannot be represented
by native job options: they are retained as an unknown `tags` option so the CLI
rejects the job instead of silently using different filtering.

Each case uses a fresh JVM process and invokes the installed, unchanged
`CppGenerator`; checked-in smoke output is not the oracle. The runner invokes
`generate-cpp` and compares its entire output path set and every byte. It invokes
an independently built `cpp_inventory` example to compare the native library's
actual `MAIN`/`COMMON` source sets and verify its file bytes against the CLI.
Only a case passing both comparisons is called an exact match. Diagnostic rows
identify the first observed guard, which can mask further unsupported features.
The complete `comments` group and the isolated interface and lambda files are
separate cases; isolated successes do not imply group compatibility.

Run with a built executable and inventory helper from the same native revision:

```sh
source /workspace/.gluecodium-env/activate
source /workspace/.ruscodium-env/activate
cd /workspace/gluecodium/ruscodium
cargo build --offline --release --example cpp_inventory
cargo build --offline --release
cd ..
ruscodium/tools/cpp-smoke-matrix/run \
  --native ruscodium/target/release/ruscodium \
  --inventory ruscodium/target/release/examples/cpp_inventory \
  --revision ACTUAL_REVISION --native-compiler "$(rustc --version)" --job-version 2 \
  --baseline ruscodium/tools/cpp-smoke-matrix/baseline.json \
  --capture /tmp/new-empty-smoke-capture --report /tmp/new-smoke-report.json
```

Choose a new empty capture directory; a nonempty case directory is rejected to
prevent stale output from affecting comparisons. `--baseline` checks each case's
inputs, options, JVM success, complete expected file hashes and source sets before
accepting the comparison. JVM, export, native rejection, inventory errors,
provenance changes and output mismatches have distinct statuses. `baseline.json`
was captured with the version-1 job and the executable built from `d9dc5b901`.
The final run uses version 2, but both represent the same loader model and JVM
outputs; schema-version rejection is not counted as a compatibility change.

The verified baseline has 1 exact match and 12 native rejections among 13
complete groups, with no JVM/export failures or output mismatches. The two
single-file comment cases are both rejected. Among complete groups the first
observed guard is an unsupported `LimeException` node in six; one each reports
an unsupported INTERNAL, JAVA, or CACHED attribute, a parent-property shape,
an external descriptor, or unsupported tags. These counts report first guards
only, not all features present in a case.

The final report measures native revision
`84377ae1ef1a68a590660893b882c500ab667ba0` using a version-2 job. The complete
groups remain at 1 exact match and 12 native rejections, with no mismatches or
JVM/export failures. The two isolated upstream documentation files each move
from native rejection to exact match, including all 20 generated files and their
source sets. The full comments group remains rejected. All 15 case input hashes,
effective options, JVM output hashes and source sets match baseline; Java,
installed JVM jar and all 315 template hashes also match. The first observed
guards for the complete groups are unchanged.

The separate [M15 report](m15.json) uses version-2 jobs and release source
`3d07f3232` after adding direct enum-backed exceptions and synchronous throws.
It retains 1 exact complete group and 12 guarded complete-group rejections;
both isolated documentation cases also remain exact matches (64 files across
the three accepted cases). No row has an output mismatch, JVM/export failure
or provenance change. All fifteen source/options/JVM output inventories and the
Java, application-jar and 315-template identities match the M11 final report.

The six complete groups previously stopped by `LimeException` now reach their
next guards: `DART` in `basic_types`, `LimeValue$Constant` in `enums`, `structs`
and `nesting`, unsupported Markdown in `comments`, and `ASYNC` in `async`.
These are first observed blockers, not complete inventories of the remaining
work. Focused native-LIME exception acceptance and executable error-code/Return
consumers are recorded separately by the
[enum-error oracle](../enum-errors-oracle/README.md).

To reproduce this comparison, use the command above with `--job-version 2`,
`--baseline ruscodium/tools/cpp-smoke-matrix/final.json`, a fresh capture
directory, a separate report path, and the actual source revision and compiler
used to build both native executables. The earlier baseline and final reports
remain historical records.
