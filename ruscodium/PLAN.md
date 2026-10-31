# Ruscodium: a staged Rust port of Gluecodium

## Goal and source of truth

Port the Gluecodium compiler itself to Rust: read LIME IDL, construct and validate
the language-independent model, and generate existing target languages. This is
not a proposal to add Rust bindings to the Kotlin compiler. Keep all committed
work for the port under the repository-root `ruscodium/` directory and leave the
existing implementation usable as a reference.

Planning baseline: commit `2044ae5c73e8b9521fac6dec6cd6133086dd4136`.
The supplied Claude conversation could not be retrieved in this environment;
no requirements have been inferred from its unseen contents. Repository code,
grammar, examples, and tests are the available specification. Incorporate any
additional requirements from that conversation when they become available.

## Findings and scope

The existing production implementation comprises 251 Kotlin source files and 315
Mustache templates across `lime-loader`, `lime-runtime`, and `gluecodium`.
There are 345 checked-in `.lime` files (18,471 lines) across smoke tests,
functional tests, CMake tests, and examples. Gluecodium generates C++ API code,
Java/Kotlin plus JNI, Swift plus CBridge, and Dart plus FFI. Replacing all of those
with verified compatibility is a migration, not a single small translation.

The first executable deliverable is a useful native compiler preview:

1. A Rust library and CLI with a real LIME frontend covering the repository's
   complete declaration and literal syntax.
2. A multi-file model with source locations, annotation/documentation retention,
   import and type resolution, and an explicitly documented set of semantic checks.
3. Deterministic JSON model output for inspection and future differential tests.
4. A guarded, standalone C++17 declaration backend for common interfaces and value
   types, exercised by compiling and using generated declarations.
5. Tests against the existing LIME corpus and targeted comparisons against the
   installed JVM implementation where available.

This first release does **not** claim drop-in Gluecodium compatibility. In
particular, generating a standalone C++ interface does not imply compatibility
with Gluecodium's JNI, CBridge, Dart FFI, or runtime ABI. Unsupported backend
features must produce a diagnostic before any outputs are written, rather than
silently dropping declarations or changing their meaning. The broader roadmap
below remains tracked after this deliverable works.

## Reference sources

- [Architecture](../docs/internal/architecture.md),
  [loader](../docs/internal/lime_loader.md),
  [resolution](../docs/internal/reference_resolution.md), and
  [validation](../docs/internal/validation.md).
- Authoritative lexical and syntactic rules:
  [`LimeLexer.g4`](../lime-loader/src/main/antlr/LimeLexer.g4) and
  [`LimeParser.g4`](../lime-loader/src/main/antlr/LimeParser.g4).
- Semantic model and name lookup:
  [`lime-runtime`](../lime-runtime/src/main/java/com/here/gluecodium/model/lime/),
  especially `LimeAmbiguityResolver.kt`.
- Existing validators, C++ name rules, and templates under
  [`gluecodium/src/main`](../gluecodium/src/main/).
- [`Calculator.lime`](../examples/calculator/lime/Calculator.lime), smoke
  fixtures, and functional inputs are acceptance examples, not specifications
  to replace with a smaller invented language.

## Architecture

Use a single Cargo package containing a reusable library and a `ruscodium`
binary. Prefer a small dependency set, with checked-in `Cargo.lock`; `serde`
and `serde_json` are reasonable for the inspectable model. No JVM subprocess
may be required by the Rust compiler. The JVM tool is only a test oracle.

Suggested module boundaries:

| Module | Responsibility |
| --- | --- |
| `source` / `diagnostic` | Source identity, byte spans, line/column rendering, structured errors |
| `lexer` | Tokens, newline boundaries, quoted identifiers, strings, comments, numbers |
| `parser` | Recursive-descent implementation of the checked-in LIME grammar |
| `model` | Owned declarations, type references, annotations, values, documents |
| `resolve` / `validate` | Symbol indexing, scope/import lookup, cycles, semantic checks |
| `generator` | Generated files in memory; deterministic JSON and guarded C++ emitters |
| CLI / IO | Sorted input discovery, options, pipeline execution, safe output writing |

Represent declarations and references without reference-counting cycles: use
stable indices or full symbol paths for resolved targets. Preserve original
spelling and spans alongside resolved identities. Separate parsing from name
resolution so files may refer forward or across input boundaries.

## First implementation milestones

### M0: establish the migration record

Create this plan and `TASKS.md` before implementation, commit them, then execute
the task list. Record evidence and scope changes as work proceeds. Use the
user-requested roles: Sol 6.1 at max effort for planning, Terra 6.1 for
implementation, and Sol 6.1 at xhigh effort for review. Commit finished logical
increments locally; no push or pull request is requested.

### M1: complete syntax frontend and source-aware model

Implement all declaration forms in `LimeParser.g4`: packages and explicit
imports; open classes, narrow interfaces, inheritance and nested declarations;
structs and fields; functions, named constructors and field constructors;
properties and accessor annotations; enums, constants, aliases, exceptions,
and lambdas with named or positional parameters. Retain external descriptors,
annotations on declarations and type references, return/throws documentation,
and declaration comments. Local `#` comments need not become model nodes.

Cover built-in, user-defined, generic and nullable types. Parse strings and
multiline strings, escapes, signed/underscored numeric literals, special floating
values, duration units, enum/constant references, positional enum values,
struct/list/map initializers, and backtick identifiers. Do not use token skipping
as a substitute for parsing a construct. Reject malformed source with a file,
line, column, and useful expected-token message. Explicitly document any
deliberate grammar deviation discovered by tests.

### M2: model loading, resolution and core validation

Discover `.lime` inputs recursively in deterministic order, support multiple
input files/directories and auxiliary inputs, and deduplicate inputs. Auxiliary
declarations participate in lookup but are not generated.

Build a global symbol index, detect duplicate non-overload declarations, and
resolve names after all files have been parsed. Match Gluecodium lookup:
collect candidates from matching explicit imports **and all enclosing paths,
including the root**, deduplicate the targets, and report ambiguity if more than
one remains. Do not assume nearest-scope shadowing. Validate imports, forward
and nested references, type-target kinds, alias cycles, and inheritance kinds
and cycles. Distinguish valid overloads from duplicate function signatures,
including alias-equivalent types where supported.

Port a useful, named set of independent checks: duplicate parameters/fields/
enumerators, invalid `Void` and nullable-`Void` positions, throws targets,
field-constructor references, and obvious invalid defaults such as `null` for a
non-nullable field. Add constant/default reference checks where implemented.
Maintain a precise compatibility table: semantic validation in the preview is
not equivalent to all Kotlin validators. JSON export should preserve parsed
features even when no code backend supports them.

### M3: native CLI and inspectable output

Provide help/version, repeated inputs and auxiliary inputs, output directory,
validation only, syntax-only/model inspection for corpus work, and explicit
generator selection. Support familiar single-dash Gluecodium spellings for the
implemented common flags, or clearly list aliases in help. Reject unknown
options and unsupported generator names with nonzero exit codes. Require an
explicit output directory for generation; validation must not write files.

JSON should have a versioned schema and stable ordering and include parsed
declarations, type/literal structure, annotation/documentation metadata, source
positions, auxiliary status, and resolved symbol identities. Use the same
library pipeline from the CLI, tests, and generators.

### M4: useful, honest C++17 generation

Generate standalone declarations for ordinary classes/interfaces (virtual
methods and destruction, named factory declarations, property accessors),
structs with fields, enums, aliases, lambdas, and basic constants/defaults.
Support nested declarations and cross-file dependencies in a deterministic
order. Map primitive types, strings, blobs, common containers, optionals, and
class/interface references to appropriate standard-library types. Document
naming and namespace rules and provide a namespace option if feasible.

Handle declaration ordering and forwards correctly for supported inputs; reject
unsatisfiable by-value dependency cycles. Detect output path/name collisions.
Implement or explicitly reject code-affecting annotations and external
descriptors. Language-specific metadata irrelevant to C++ may be retained
without affecting C++ generation, but generic or C++ attributes must not be
silently ignored. Likewise, reject unsupported throwing/error-code behavior,
runtime-dependent types, or initializers rather than inventing compatibility.

The calculator must at least parse, resolve, validate under the documented
checks, and export JSON. Its throwing methods can remain an explicit C++ backend
limitation until Gluecodium's `Return`/error-code runtime is ported. Compile and
use a separate representative generated C++ fixture with classes/interfaces,
structs, collections/optionals, nesting, aliases, and multiple input files.
Include a checked-in repository fixture in C++ acceptance where its features
fall within this backend's contract.

### M5: verification, review and handoff

- `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, and
  `cargo test` from `ruscodium/`.
- Parse all 345 baseline `.lime` files individually, with exact file count
  assertions or an explained inventory; no blanket ignores or exclusions.
  Parsing them as a single model is invalid because many fixtures deliberately
  reuse qualified names in separate test scenarios.
- Resolve/validate coherent fixture groups separately, including the calculator
  and selected real functional/smoke groups with their auxiliary sources.
- Test malformed strings/comments/declarations, unresolved and ambiguous names,
  import collisions, duplicate declarations/signatures, alias/inheritance
  cycles, and unsupported-backend errors. Verify failure produces no partial
  generated output and repeated output is deterministic.
- Compile generated C++ with `-std=c++17 -Wall -Wextra -Werror` where a compiler
  is available and execute a small program using generated declarations.
- Compare selected validation successes and failures with the installed JVM
  Gluecodium (`-input ... -validate`), especially import-vs-local ambiguity.
  Report differences honestly; passing parser corpus tests is not output parity.
- Run the requested independent review, fix material findings, update tasks and
  compatibility documentation, and commit the tested result.

## Roadmap to full Gluecodium compatibility

| Stage | Work remaining after the preview | Required evidence |
| --- | --- | --- |
| Frontend fidelity | Complete all Kotlin validators, filtering/tags, full attribute semantics, Limedoc references/placeholders, warnings/strict mode | Differential model and diagnostic cases from existing unit tests |
| C++ parity | Name-rule files, every C++ attribute, constructors/accessors/equality, constants, external types, `Return`, error categories, runtime helpers, API/internal outputs | Existing C++ golden outputs and functional C++ tests |
| Runtime and binding core | Common conversion/runtime model, name resolvers, ownership, cache and lifetime contracts | Native conversion and lifetime regression tests |
| Android | Java/Kotlin source and JNI, platform annotations, async decorators, parcelable behavior | Existing Android smoke outputs and functional tests |
| Apple | Swift source and CBridge, nullable/external/generic/ownership behavior | Existing Swift smoke outputs and platform functional tests |
| Dart | Dart source, FFI runtime, finalizers, async and ownership semantics | Existing Dart smoke outputs and functional tests |
| Tooling compatibility | Options files, all CLI options, caching/stale-file handling, split outputs, CMake/Gradle integration and distribution | Existing launcher/build integration tests and packaging checks |
| Cutover | Define compatibility guarantees, publish migration guide, performance measurement and release policy | Full supported-platform parity matrix before replacing the JVM tool |

Preserve the preview's stable public boundaries where practical, but avoid
declaring its JSON schema or C++ ABI final before the corresponding parity work.
