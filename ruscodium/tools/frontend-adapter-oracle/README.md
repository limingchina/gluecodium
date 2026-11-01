# Native frontend to C++ adapter oracle

`check` builds a verification-only example and the ordinary CLI, and invokes
the existing unchanged JVM `CppGenerationOracle` in a fresh process for each
case. It copies the three original LIME inputs into a temporary working tree;
mutations touch only those copies. The Java classes and installed JVM library
are reused, not duplicated. The native pipeline receives LIME and options,
never a JVM job, snapshot, generated inventory, or expected file.

```sh
source /workspace/.ruscodium-env/activate
source /workspace/.gluecodium-env/activate
python3 -m unittest discover -s ruscodium/tools/frontend-adapter-oracle -p 'test_*.py'
ruscodium/tools/frontend-adapter-oracle/check
# Optional focused subsets: check --core-only, check --docs-only, or
# check --case=documentation-blocks.
```

Requirements are Rust, Python 3, a Java 17 JDK, the installed distribution at
`gluecodium/build/install/gluecodium/lib`, and a C++17 compiler (`CXX` can
select it). Baselines compare every output path, source set and byte with both
the live JVM and checked-in captures: 26 default and 24 custom. Both library
and CLI outputs compile and run the existing consumers with `-std=c++17
-Wall -Wextra -Werror`. The CLI runs in the temporary working directory with an
empty `PATH`, receiving real LIME, templates and options. Additional fresh JVM
jobs test renamed packages/types, values and alias ordering, generic and
nullable references, auxiliary lookup and ownership, open/narrow declarations,
constructors, static/struct methods, numeric literals, and `@Cpp` names on
nested structs, fields, methods, parameters, properties, aliases, enums and
enumerators. They compare all
generated output and the same model projection, rather than merely expecting a
change. The original captures are never used as native generator inputs.
The documentation-blocks mutation also covers Unicode, paragraphs, platform
selection, exclusion, struct constructor comments, and field documentation
used in generated field-constructor parameter comments. Explicit `@param` on a
field constructor remains rejected by the native frontend.

The two upstream `CommentsInterface.lime` and `CommentsLambda.lime` files are
also loaded independently by each frontend. Their 40 generated files and source
sets are compared to the live JVM and the frozen M11 captures; both library
and empty-PATH CLI outputs compile and run the corresponding strict consumers.
The live JVM comparison uses those unchanged main files without the unrelated
auxiliary directory or configured-but-unused placeholders present in the
original M11 captures. The core custom case separately checks ordered auxiliary
membership and lookup. This does not claim native support for placeholder
configuration or all M11 documentation fixtures.

`project.py JOB` exports the comparison projection. It checks each node class
and its complete property key set against an explicit schema, rejecting unknown
classes or fields. It records ordered main/auxiliary roots and member categories,
paths (including package and disambiguator), kinds, attributes, comments,
external facts, direct and resolved type targets, nullable edges, generic
arguments, alias chains, child types, parameters and returns, accessors,
static/constructor flags, defaults, enumerators, constructor field/struct
links, reference-map membership, builtin type IDs and filename ownership by
basename (the fixtures use distinct basenames; ambiguous basenames fail).
Paths are also used as declaration identities. The separate source-set
inventory and options are verified through the whole-file comparisons; source
physical prefixes and spans are excluded from the model projection.

Traversal IDs, allocation order and equivalent copies of builtins and generic
getter views are normalized structurally. Reference-wrapper implementation
classes and cached full-name strings are normalized to their resolved semantic
targets; nullable edges and alias declarations remain separate. The `actualType`
getter's target is checked against the independently traversed alias chain, and
unrecognized getter properties fail closed. Named type and constructor field
links must refer to the object indexed under their declaration path, preventing
a separate same-path object from hiding changed declarations. The projection
uses comment contents from v2 raw sections or v1's measured empty getter, and
fails if emptiness is unavailable or placeholders are present. Adjacent ordinary
raw fragments with the same tag are concatenated, preserving their text and tag
transitions, to normalize JVM tokenization against contiguous native text. The
normalizer never concatenates `Placeholder` fragments, whose keys and recursive
selection have distinct semantics; placeholder-bearing jobs are rejected by
this bounded projection. This is bounded evidence for the enumerated
model facts, not a claim of a complete canonical model or arbitrary getter
equivalence. `test_project.py` checks that changed root order, reference-map
membership, direct nullability, builtin IDs, constructor link attributes,
same-path cloned declarations and unrecognized fields are
detected.
