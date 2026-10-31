# Template surface inventory

`tools/template_surface.py` inventories the unchanged production Trimou sources under `gluecodium/src/main/resources/templates`. It is a migration aid, not a template interpreter or a model specification. It needs Python 3 and no third-party packages.

```sh
cd ruscodium
python3 tools/template_surface.py --summary
python3 tools/template_surface.py --output /tmp/template-surface.json
python3 -m unittest discover -s tools/tests -v
```

Use `--root DIR` to scan fixtures or another checkout. Full JSON includes per-file SHA-256, candidate paths, helper invocations, selector arguments, and partial references, each with a template-relative file and one-based line. Output order is deterministic. The corpus hash is SHA-256 of the UTF-8 concatenation of each sorted relative filename, a NUL byte, its lowercase hexadecimal file hash, and a newline. Compare it before using the counts as a baseline.

The current corpus contains 315 templates: cbridge 31, common 3, cpp 48, dart 48, ffi 37, java 30, jni 51, kotlin 30, swift 36, and xml 1. Corpus SHA-256: `aa647ae41a7f657b955c60550c688dfe0a19054e15a9431dd6724cb78ce99d49`. The lexical scan records 4,815 property candidates, 5,227 helper calls, 1,866 partial/include references and inline definitions, and 3,110 selector-bearing calls; `resolveName` accounts for 2,499 calls. Counts are occurrences, not unique paths or proven runtime accesses.

A candidate can be a section, value, positional argument, or unquoted named assignment value; quoted strings, literals, closing tags, and comments are excluded. `possible_local` means its first component is assigned by a `#set` somewhere in that file, a deliberately conservative file-wide approximation; `context` identifies `this`, `this.*`, `@` variables and relative paths. Other entries are `candidate_property`, which can still resolve to a local, a parent context, a resolver, or a non-model value. The scanner cannot infer receiver types, scope, runtime values, reflection behavior, or the complete model surface. `eval` and other selectors can introduce dynamic lookups: their original arguments are recorded separately, including quoted keys, modes, predicate names, and assignment arguments. The helper lists follow `TemplateEngine.kt` plus common Trimou control helpers. The installed Trimou 2.5.1 `HelpersBuilder` class names the equality helpers `isEq` and `isNotEq`; these correspond to the builder calls `addIsEqual` and `addIsNotEqual`. A corpus audit found no remaining unknown heads with arguments; they are a maintained lexical classification, not runtime registration discovery. Unrecognized names are treated as paths.

Partials record direct `>` references, `+` inline partial definitions, and selectors supplied to `prefixPartial`, `joinPartial`, and `include`; dynamic selectors are marked. This is a syntactic dependency inventory, not a resolved graph: helper behavior, runtime values, relative lookup, aliases and whether an `include` value names a template require engine-specific analysis. Quoted partial selectors remain quoted in JSON. The scanner assumes the corpus's standard delimiters and simple Trimou token syntax; it does not validate templates, parse arbitrary nested expressions, execute helpers, or resolve partials. Review the JSON evidence and engine implementation before implementing a compatible data model.

The engine choice for a full port remains open. The reference config uses Trimou with a bracket/dot key splitter, disabled value escaping, registered helpers, and a copyright resolver. Retaining template syntax or converting it requires separate compatibility evaluation; helper behavior, dynamic lookups, whitespace, and byte-for-byte generated output need differential tests. This inventory does not establish backend parity. The current Rust frontend and guarded C++ preview are not byte-identical Gluecodium generation.
