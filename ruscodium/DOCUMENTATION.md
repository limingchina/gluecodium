# Native C++ documentation

Version-2 `gluecodium.cpp-generation-job` inputs extend the snapshot job described
in [GENERATION.md](GENERATION.md) with a required `raw_comments` object. Its keys
must be exactly the IDs of all `LimeComment` nodes in the snapshot, including
empty comments and placeholder targets. Each value is an ordered list of
two-string `[tag, text]` pairs. For example:

```json
"raw_comments": {
  "n12": [["", "Shared text. "], ["Cpp", "C++ text."]],
  "n13": []
}
```

The node's path, exclusion flag and placeholder-reference map remain in the
reference snapshot. Version 2 forbids comment `isEmpty` overlays and accepts no
selected text, formatted Doxygen, or comment predicate results. Version 1 rejects
`raw_comments` and retains its measured-empty-comment contract.

The JVM oracle exports the private ordered `LimeComment.taggedSections` field
through a narrowly scoped, checked reflection adapter. These are raw model facts,
not formatted output. Those captured snapshots and allowed getter views come
from the JVM frontend. The separate [native adapter](FRONTEND_ADAPTER.md)
constructs raw comments from its bounded native source parser; the two paths
share the same backend formatter.

Rust derives three different views. Raw `isEmpty` tests whether every section's
payload is empty, across all platforms. Selected C++ text concatenates universal,
exact `Cpp`, and `Placeholder` sections in order, recursively substitutes the
referenced comments, and applies Kotlin's trimming rules at each expansion.
Comment predicates check the selected text and the upstream exclusion rules.
Thus a Java-only comment can be globally nonempty yet supply no C++ text.

The formatter admits plain Unicode prose, paragraphs and measured newline and
spacing behavior. It preserves soft line breaks and does not wrap long lines.
Markdown/link processing remains guarded, including emphasis, code, headings,
lists, tables, HTML, documentation references and unproved control/whitespace
forms. Guards apply after platform selection and placeholder expansion. A plain
comment cannot bypass them by importing a formatted answer. Raw exclusion,
function/parameter/return documentation, property documentation and constructor
comments use the unchanged upstream C++ templates.

Admission is intentionally conservative: characters such as underscores,
asterisks, brackets, backticks, angle brackets, braces, ampersands, backslashes,
hashes, tildes and vertical bars reject even where they could be literal prose.
Controls other than LF and measured tab cases are rejected. Trailing tabs,
paragraph-initial code indentation and paragraph-final hard breaks before a
blank line are also guarded. These restrictions describe the currently proven
formatter profile, not the complete Markdown grammar.

Missing or malformed raw records, invalid placeholder references, cycles and
excessive expansion fail before output writes. Expansion is bounded by depth
and size (128 levels and 1 MiB of selected text), with memoization for repeated
placeholder references. Other existing
unsupported model features remain rejected. Write-phase I/O failures retain the
limitations documented in [GENERATION.md](GENERATION.md).

The [documentation oracle](tools/cpp-generation-oracle/README.md) compares
complete JVM-generated files and runs C++ consumers. It includes separately
loaded, unmodified `CommentsInterface.lime` and `CommentsLambda.lime` inputs and
a focused fixture for platform sections, Unicode, paragraphs, configured
placeholders, exclusion and member/constructor documentation. Configured loader
placeholders are one level deep; recursive raw-graph tests are separate evidence.
The three fixtures contain 63 complete output files: 23 in the focused job and
20 in each upstream-file job, including all eighteen helper/export files per
job. All paths, source sets and UTF-8 bytes are compared.
The [smoke inventory](tools/cpp-smoke-matrix/README.md) reports complete-group
results separately from these per-file cases. Full Markdown, scoped documentation
links and complete native frontend/documentation parity remain future work.
