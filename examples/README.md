## Overview

[README.md](../README.md) in the root provides basic information about Gluecodium.
The examples expose shared C++ APIs to Java, Swift and Python. Native code is built
into a shared library for Android and Apple, or a CPython extension for Python.
The examples use simple configurations. For more advanced setups, check `cmake/tests/unit`.


## Build and publish gluecodium

The Android and Apple examples use Gluecodium from the local Maven repository.
Build and publish it from the repository root:

```
./gradlew publishToMavenLocal
```

The Python client uses a local CLI distribution. Build it from the repository root:

```
./gradlew :gluecodium:installDist
```

## CMake Gluecodium wraper.

This is a set of CMake functions which provide the following functionality:
- Download Gluecodium from artifactory.
- Add step to generate code.
- Set options to configure generated code.
- Help to configure a target to include generated C++/Swift/Java/Flutter/Python sources, add include directories, etc.
- Build a CPython extension with pybind11.

While the examples work with the shipped CMake Gluecodium wrapper for a real application it's handy to clone only the subtree `cmake/modules`.

## Example `calculator`.

What this example demonstrates:
- How to configure the project to generate C++, Java, Swift and Python source code.
- How to use the generated code in Android and iOS applications and a Python client.
- How to describe basic primitives like `class`, `interface`, `struct` and how to interact with them.
- How to make platform-only comments and links.

What this example DOESN'T demonstrate:
- How to make complex build setup with several modules.
- How to describe custom types.
- How to make a Flutter plugin.
- How to use advanced Gluecodium features such as tags, advanced manipulations with comments or properties.

All clients share [calculator/lime/Calculator.lime](calculator/lime/Calculator.lime)
and [calculator/cpp/CalculatorImpl.cpp](calculator/cpp/CalculatorImpl.cpp).
For a detailed description and platform build instructions, check
[calculator/README.md](calculator/README.md) and the
[Python client instructions](calculator/python/README.md).
