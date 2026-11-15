# C++ completion oracle

The smoke runner discovers every upstream smoke directory and captures the real
JVM C++ generator's full file paths, bytes, and MAIN/COMMON source sets. It
checks at least 49 total directories, 38 with C++ references and both expected
strict-validation failures; the other eleven receive explicit JVM outcomes.
The functional runner captures all 45 C++ feature groups as one coherent model
with 115 LIME sources, plus the custom naming model and focused regression
fixtures. Both compare the complete JVM output against native snapshot and
real-LIME generation, including source sets, without normalizing bytes.

The JVM exporter retains external descriptors, positional enum indexes and
unresolved ambiguous reference facts in its unfiltered model. It does not feed
JVM computed getter overlays into native generation. It saves independent JVM
files before attempting export. Both runners pin their native executables and
record before/after source, template, tool and JVM jar hashes and git identity.
A run exits nonzero if an acceptance case fails or source identity changes.

With Java 17 and the Rust toolchain active, build the native executable and
`cpp_inventory` and `cpp_completion_inventory` examples, then run:

```sh
ruscodium/tools/cpp-completion/check \
  --native ruscodium/target/release/ruscodium \
  --snapshot-inventory ruscodium/target/release/examples/cpp_inventory \
  --lime-inventory ruscodium/target/release/examples/cpp_completion_inventory \
  --gtest-source /workspace/.cpp-test-tools/googletest \
  --capture /tmp/new-empty-cpp-completion \
  --revision "$(git rev-parse HEAD)" --native-compiler "$(rustc --version)"
```

The driver also runs the pinned 652-example CommonMark formatter comparison and
compiles all generated and upstream handwritten functional C++ and all ten
upstream GTest sources. The pinned CommonMark specification attribution is in
`commonmark/ATTRIBUTION.md`. Strict builds and compatibility builds are separate:
the latter record explicit upstream warning exceptions (`reorder`,
`unused-parameter`, `sign-compare`, `unused-result`, `unused-variable`) and forced `<cstdint>` for known JVM output
and source issues. Strict failures remain failures when compatibility succeeds.
The naming consumer similarly records an upstream unused-parameter warning and
runs a separately labeled compatibility compile. The aggregate gate accepts
these strict failures only after `consumer-parity.py` matches the known
source, line, and diagnostic catalog and compares every JVM/native compilation
and runtime result. The strict reports themselves remain failed.

Use `functional-inventory --output DIR` to regenerate the feature/source
inventory and Java-properties manifests. Individual `run`, `functional-check`,
`markdown-check`, `compile-functional.py` and `compile-namerules.py` commands
can be invoked independently. Historical M11/M15 reports remain unchanged.
