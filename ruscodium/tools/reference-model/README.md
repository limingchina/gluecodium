# Experimental JVM reference snapshot

This tool loads LIME with the existing JVM loader and captures a versioned JSON graph for investigation and golden fixtures. The [native template runtime](../../TEMPLATES.md) imports this bounded version-1 snapshot as an identity graph. The snapshot is distinct from Rust preview-model JSON; neither a complete canonical adapter nor an adapter from the native preview model is provided. This is not a compatibility guarantee, and the exporter does not add a JVM dependency to the Rust runtime.

Build the JVM distribution first (the expected libraries are `gluecodium/build/install/gluecodium/lib/*.jar` relative to the repository root). Java 17 is required. Set `JAVA_HOME` to a JDK 17 installation, or put `java` and `javac` on `PATH`. The script compiles into a temporary directory and removes it afterward.

Run from any directory; source paths are interpreted relative to the repository root:

```sh
ruscodium/tools/reference-model/export --main examples/calculator/lime/Calculator.lime --output /tmp/calculator-reference.json
ruscodium/tools/reference-model/export --main path/to/main.lime --aux path/to/aux.lime > /tmp/reference.json
ruscodium/tools/reference-model/test
```

Repeat `--main` and `--aux` for more sources. Without `--output`, the completed document goes to stdout; diagnostics go to stderr. Load, getter, unsupported value, or serialization errors fail before the output file is opened. Missing paths, non-LIME files, and inputs containing no `.lime` files fail before output. The loader performs its usual validation. The tool passes no documentation placeholders.

## Schema version 1

The document has `schema: "gluecodium.reference-model.snapshot"`, `version: 1`, a `root` reference to `LimeModel`, and `nodes`. Each node has an `id`, its fully qualified JVM `class`, and a `properties` object. A model object occurrence is represented by `{"$ref":"n..."}`; IDs identify instances and cycles and are assigned in traversal order. Scalars, null, lists, and string-keyed maps retain their JSON structure. Enums are `{"enum":"fully.qualified.Class","name":"CONSTANT"}`. The root exposes `referenceMap`, `topElements`, `auxiliaryElements`, and `fileNameMap` through the same property rules. Keys and properties are sorted; list order is preserved. Values in `fileNameMap` beneath the repository root are normalized to repository-relative paths; other strings are preserved. Use consistent repository-relative source arguments for reproducibility.

Coverage is deliberately bounded: for classes in `com.here.gluecodium.model.lime`, public zero-argument instance getters corresponding to non-static, non-synthetic backing fields are read, including inherited fields. Private implementation fields, computed-only getters, companion objects, caches, and methods are excluded. Two computed semantic edges are explicitly included: `element` on `LimeElementRef` and `type` on `LimeTypeRef`; resolving an invalid reference fails the export. `LimeAttributes` is another special case: its public typed API exports an `attributes` property keyed by attribute and value enum names, including empty attribute maps. Model objects are traversed once by identity. Other object types, non-string map keys, non-finite numbers, and throwing selected getters fail with a property path instead of being stringified or silently omitted. In particular, computed comment text and external descriptor platform information can be absent: this snapshot does not include every template-visible computed property. Source directories are expanded to sorted absolute `.lime` paths before loading (directory symlinks are not followed); overlapping main and auxiliary paths retain the loader’s main-source precedence. JVM/library version and source order within loader-created lists may affect results; compare snapshots made with the same distribution and inputs.

The port’s baseline corpus excludes `ruscodium/`, including the intentionally invalid test fixture in this directory.
