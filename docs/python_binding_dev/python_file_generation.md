---
Python Module Filename Derivation in Gluecodium — Architecture Document

Overview

The Gluecodium Python code generator produces two categories of output files for each LIME type:
1. A Python wrapper (.py) that exposes the type to Python users.
2. A Python stub (.pyi) that provides type hints.
3. A pybind11 C++ binding (.cpp) that wires the C++ API to Python.

The filename for each type is determined by a chain of four components, all of which converge in PythonNameRules.

---
Key Source Files

File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGenerator.kt
Role: Main generator; calls getPythonFileName(), getPythonStubFileName(), getPybind11FileName() to produce GeneratedFile objects. Also contains getPythonTypes() which performs
duplicate-filename detection.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonNameRules.kt
Role: Central file for filename logic. Contains getPythonFileName(), getPythonStubFileName(), getPybind11FileName(), and the getName() override that decides the filename stem.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonNameResolver.kt
Role: Resolves Python-side type names and dotted module import paths (e.g., test.SomeEquatableClass).
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/java/com/here/gluecodium/generator/python/Pybind11NameResolver.kt
Role: Resolves C++ names used inside the generated pybind11 .cpp binding files.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonImportResolver.kt
Role: Builds the import path used in from X import Y statements; mirrors the filename logic.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGeneratorPredicates.kt
Role: Template predicates used by mustache templates (e.g., isNestedInternal, isAncestorField).
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/resources/namerules/python.properties
Role: Configuration file: type=UpperCamelCase, error.suffix=Error, join.infix=_.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/lime-runtime/src/main/java/com/here/gluecodium/model/lime/LimePath.kt
Role: Defines head (package prefix), tail (nested element hierarchy), hasParent (tail.size > 1), name, container.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/lime-runtime/src/main/java/com/here/gluecodium/model/lime/LimeType.kt
Role: Abstract base for all LIME types (structs, classes, interfaces, enums, exceptions, lambdas).
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/java/com/here/gluecodium/generator/common/NameRules.kt
Role: Base class; maps LIME element kinds to name-transform functions from a NameRuleSet.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/java/com/here/gluecodium/generator/common/NameRuleSet.kt
Role: Holds per-kind name-transform lambdas (e.g., getTypeName, getMethodName). Configured from .properties files.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/java/com/here/gluecodium/generator/common/NameRuleSetLoader.kt
Role: Reads .properties files and constructs a NameRuleSet.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/java/com/here/gluecodium/generator/common/templates/TemplateEngine.kt
Role: Maps template names like "python/PythonFile" to mustache files on the classpath.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/resources/templates/python/PythonFile.mustache
Role: Template for the generated Python .py wrapper file.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/resources/templates/python/Pybind11File.mustache
Role: Template for the generated pybind11 .cpp binding file.
────────────────────────────────────────
File: /Volumes/APFS/Work/gluecodium/gluecodium/src/main/resources/templates/python/PythonStub.mustache
Role: Template for the generated .pyi stub file.

---
The Filename Derivation Chain

Step 1: LimePath (the Lime model's path)

Every LIME element has a LimePath with two lists:

- head: The package/namespace prefix (non-traversable). Example: ["com", "example"].
- tail: The nesting hierarchy (traversable). Example: for OuterClass.InnerClass, tail = ["OuterClass", "InnerClass"].
- hasParent: tail.size > 1 — true for nested types (a type inside another type).
- name = tail.last() — the simple element name.

Step 2: PythonNameRules.getName() — the filename stem

override fun getName(limeElement: LimeElement) =
    getPlatformName(limeElement as? LimeNamedElement)        // 1. @Python(Name=...)
        ?: if (limeElement is LimeType && limeElement.path.hasParent) {
            limeElement.path.tail.joinToString("")          // 2. Nested type: concatenate tail
        } else {
            super.getName(limeElement)                       // 3. Top-level type: apply name rule
        }

Three tiers:
1. @Python(Name = "...") — overrides the name entirely.
2. Nested types (hasParent = true) — the name is the raw concatenation of all tail segments. OuterClass.InnerClass becomes "OuterClassInnerClass".
3. Top-level types — the base NameRules.getName() calls ruleSet.getTypeName(name), which applies UpperCamelCase from python.properties. So some_equatable_class becomes "SomeEquatableClass".

Step 3: PythonNameRules.getPythonFileName() — the full file path

fun getPythonFileName(limeElement: LimeNamedElement): String {
    val packagePath = limeElement.path.head.joinToString(File.separator)
    return PYTHON_TARGET_DIRECTORY + packagePath + File.separator + getName(limeElement) + ".py"
}

Where PYTHON_TARGET_DIRECTORY = "python/".

Result: python/<package_path>/<TypeName>.py

Step 4: getPybind11FileName() — the C++ binding file path

fun getPybind11FileName(limeElement: LimeNamedElement): String {
    val packagePath = limeElement.path.head.joinToString("_")  // underscore-joined, not separator
    return PYBIND11_TARGET_DIRECTORY + packagePath + "_" + getName(limeElement) + ".cpp"
}

Where PYBIND11_TARGET_DIRECTORY = "python/pybind11/". Note that packagePath uses _ as separator, not File.separator.

Result: python/pybind11/<package_path>_<TypeName>.cpp

Step 5: Import paths (mirrors the file path)

In PythonImportResolver.createImport():
val modulePath = (limeElement.path.head + nameResolver.resolveName(limeElement)).joinToString(".")

Result: <package>.<TypeName> (dot-separated), e.g., test.SomeEquatableClass.

---
Worked Examples

Top-level type SomeEquatableClass in package test:
- path.head = ["test"], path.tail = ["SomeEquatableClass"], hasParent = false
- getName() = "SomeEquatableClass" (UpperCamelCase applied to LIME name)
- Python file: python/test/SomeEquatableClass.py
- Stub file: python/test/SomeEquatableClass.pyi
- Pybind11 file: python/pybind11/test_SomeEquatableClass.cpp
- Import path: test.SomeEquatableClass

Nested type OuterClass.InnerClass in package test:
- path.head = ["test"], path.tail = ["OuterClass", "InnerClass"], hasParent = true
- getName() = "OuterClassInnerClass" (raw tail concatenation)
- Python file: python/test/OuterClassInnerClass.py
- Pybind11 file: python/pybind11/test_OuterClassInnerClass.cpp
- Import path: test.OuterClassInnerClass

Type with @Python(Name = "...") — the attribute overrides everything; the file stem becomes exactly the specified name.

---
Duplicate Filename Detection

In PythonGenerator.getPythonTypes() (line 454), after collecting all types, the code groups them by nameRules.getPythonFileName(it) and detects duplicate filenames. Non-major types (lambdas, type aliases) that collide are filtered out; major types (structs, enums, classes, interfaces, exceptions) that collide are retained but flagged. This is a safety net for edge cases in the LIME model.

---
Template Files (Mustache)

All are under /Volumes/APFS/Work/gluecodium/gluecodium/src/main/resources/templates/python/:

┌─────────────────────────────────────┬──────────────────────────────────────────────────────────┐
│              Template               │                         Purpose                          │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonFile.mustache                 │ Main Python .py wrapper; imports + type-specific content │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11File.mustache               │ C++ pybind11 .cpp binding file                           │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonStub.mustache                 │ .pyi stub file (minimal, just imports + content)         │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonClass.mustache                │ Python class wrapper                                     │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonStruct.mustache               │ Python struct wrapper                                    │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonInterface.mustache            │ Python interface wrapper                                 │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonEnumeration.mustache          │ Python enum wrapper                                      │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonException.mustache            │ Python exception wrapper                                 │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonLambda.mustache               │ Python lambda wrapper                                    │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonTypeAlias.mustache            │ Python type alias                                        │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11Class.mustache              │ pybind11 class binding                                   │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11Struct.mustache             │ pybind11 struct binding                                  │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11Enum.mustache               │ pybind11 enum binding                                    │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11Interface.mustache          │ pybind11 interface binding                               │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11Exception.mustache          │ pybind11 exception binding                               │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11Lambda.mustache             │ pybind11 lambda binding                                  │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11TypeAlias.mustache          │ pybind11 type alias binding                              │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11ModuleInit.mustache         │ PYBIND11_MODULE entry point (registers all types)        │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11WrapperCache.mustache       │ C++ wrapper cache for identity preservation              │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11ReturnCaster.mustache       │ C++ return type caster (Return<T, Error>)                │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11GenericCaster.mustache      │ Generic C++ caster                                       │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonNativeBase.mustache           │ Python _native_base.py                                   │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonSetupPy.mustache              │ setup.py template                                        │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonSetupPy.mustache              │ setup.py template                                        │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonSetupPy.mustache              │ setup.py template                                        │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonSetupPy.mustache              │ setup.py template                                        │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonPyproject.mustache            │ pyproject.toml template                                  │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonStubException.mustache        │ Stub for exception types                                 │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonStubClass.mustache            │ Stub for class types                                     │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonStubStruct.mustache           │ Stub for struct types                                    │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonStubInterface.mustache        │ Stub for interface types                                 │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonStubEnumeration.mustache      │ Stub for enum types                                      │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonStubFunction.mustache         │ Stub for function types                                  │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonStubLambda.mustache           │ Stub for lambda types                                    │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonStubTypeAlias.mustache        │ Stub for type alias types                                │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonField.mustache                │ Python struct/class field                                │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonProperty.mustache             │ Python property                                          │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonFunction.mustache             │ Python function                                          │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ PythonInit.mustache                 │ __init__.py file content                                 │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11TrampolineFunction.mustache │ Trampoline for overrideable methods                      │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11TrampolineProperty.mustache │ Trampoline for overrideable properties                   │
├─────────────────────────────────────┼──────────────────────────────────────────────────────────┤
│ Pybind11GenericCaster.mustache      │ Generic C++ type caster                                  │
└─────────────────────────────────────┴──────────────────────────────────────────────────────────┘

---
Summary of the Three Decisions

1. Directory structure: determined by path.head (the LIME package), joined by File.separator.
2. Filename stem: determined by getName() — either @Python(Name=...), raw tail concatenation for nested types, or UpperCamelCase name rule for top-level types.
3. File extension: .py for Python wrappers, .pyi for stubs, .cpp for pybind11 C++ bindings.
