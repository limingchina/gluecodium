

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Hash.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/CompressionState.h"
#include "smoke/Rectangle.h"
#include "smoke/UseDartExternalGenerics.h"
#include "unordered_map"
#include "unordered_set"
#include "vector"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using UseDartExternalGenerics = ::smoke::UseDartExternalGenerics;


void register_UseDartExternalGenerics(py::module_& module) {
    py::class_<UseDartExternalGenerics, std::shared_ptr<UseDartExternalGenerics>>(module, "UseDartExternalGenerics")
        .def("use_generics", &UseDartExternalGenerics::use_generics, py::arg("list"), py::arg("set"))

        ;
}

