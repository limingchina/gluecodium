# Experimental JVM reference snapshot

This tool loads LIME with the existing JVM loader and captures a versioned JSON graph for investigation and future golden fixtures. It is a reference-model snapshot, not the Rust AST JSON format; there is no importer or compatibility guarantee. It does not add a JVM dependency to the Rust backend.

Build the JVM distribution first (the expected libraries are `gluecodium/build/install/gluecodium/lib/*.jar` relative to the repository root). Java 17 is required. The script defaults to `/workspace/.gluecodium-env/jdk-17.0.16+8`; set `JAVA_HOME` to use another Java 17 installation. The script compiles into a temporary directory and removes it afterward.

Run from any directory; source paths are interpreted relative to the repository root:

```sh
ruscodium/tools/reference-model/export --main examples/calculator/lime/Calculator.lime --output /tmp/calculator-reference.json
ruscodium/tools/reference-model/export --main path/to/main.lime --aux path/to/aux.lime > /tmp/reference.json
ruscodium/tools/reference-model/test
```

Repeat `--main` and `--aux` for more sources. Without `--output`, the completed document goes to stdout; diagnostics go to stderr. Load, getter, unsupported value, or serialization errors fail before the output file is opened. The loader performs its usual validation. The tool passes no documentation placeholders.

## Schema version 1

The document has `schema: "gluecodium.reference-model.snapshot"`, `version: 1`, a `root` reference to `LimeModel`, and `nodes`. Each node has an `id`, its fully qualified JVM `class`, and a `properties` object. A model object occurrence is represented by `{"$ref":"n..."}`; IDs identify instances and cycles and are assigned in traversal order. Scalars, null, lists, and string-keyed maps retain their JSON structure. Enums are `{"enum":"fully.qualified.Class","name":"CONSTANT"}`. The root exposes `referenceMap`, `topElements`, `auxiliaryElements`, and `fileNameMap` through the same property rules. Keys and properties are sorted; list order is preserved. Absolute file paths beneath the repository root are normalized to repository-relative paths. Use consistent repository-relative source arguments for reproducibility.

Coverage is deliberately bounded: for classes in `com.here.gluecodium.model.lime`, public zero-argument instance getters corresponding to non-static, non-synthetic backing fields are read, including inherited fields. Private implementation fields, computed-only getters, companion objects, caches, and methods are excluded. `LimeAttributes` is a special case: its public typed API exports an `attributes` property keyed by attribute and value enum names, including empty attribute maps. Model objects are traversed once by identity. Other object types, non-string map keys, non-finite numbers, and throwing selected getters fail with a property path instead of being stringified or silently omitted. In particular, this snapshot is not a promise to include every template-visible computed property. JVM/library version, source list and source order within loader-created lists may affect results; compare snapshots made with the same distribution and inputs.
